"""Markdown 转微信内联样式 HTML。

公众号正文不支持外部 CSS，这里把常见 Markdown 语法直接转成
带内联样式的 HTML 片段，保证可原样推送到草稿箱。
"""
import re

# 配色方案：heading=标题色，accent=强调/链接色，quote_bg=引用底
SCHEMES = {
    "default":  {"name": "默认蓝",   "heading": "#1f2329", "accent": "#3370ff", "quote_bg": "#f2f3f5"},
    "business": {"name": "商务蓝",   "heading": "#12304a", "accent": "#1a6bff", "quote_bg": "#eef3fb"},
    "warm":     {"name": "温暖橙",   "heading": "#7a3b00", "accent": "#ff7a00", "quote_bg": "#fff4e6"},
    "fresh":    {"name": "清新绿",   "heading": "#14532d", "accent": "#16a34a", "quote_bg": "#ecfdf3"},
    "elegant":  {"name": "优雅紫",   "heading": "#4c1d95", "accent": "#7c3aed", "quote_bg": "#f5f0ff"},
    "minimal":  {"name": "极简黑白", "heading": "#111111", "accent": "#111111", "quote_bg": "#f7f7f7"},
}


def list_schemes():
    return [{"key": k, "name": v["name"]} for k, v in SCHEMES.items()]


def _escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(text, s):
    text = _escape(text)
    # 图片 ![alt](url)
    text = re.sub(
        r'!\[([^\]]*)\]\(([^)\s]+)\)',
        lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" '
                  f'style="max-width:100%;border-radius:8px;display:block;margin:12px auto;">',
        text,
    )
    # 链接 [text](url)
    text = re.sub(
        r'\[([^\]]+)\]\(([^)\s]+)\)',
        lambda m: f'<a href="{m.group(2)}" style="color:{s["accent"]};text-decoration:none;">{m.group(1)}</a>',
        text,
    )
    # 行内代码 `code`
    text = re.sub(
        r'`([^`]+)`',
        r'<code style="background:#f2f3f5;color:#d63384;padding:2px 6px;border-radius:4px;font-size:0.9em;">\1</code>',
        text,
    )
    # 加粗 ** ** 或 __ __
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong style="font-weight:700;">\1</strong>', text)
    text = re.sub(r'__([^_]+)__', r'<strong style="font-weight:700;">\1</strong>', text)
    # 斜体 * *
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em style="font-style:italic;">\1</em>', text)
    return text


def markdown_to_html(md, theme="default"):
    s = SCHEMES.get(theme, SCHEMES["default"])
    lines = md.split("\n")
    out = []
    i, n = 0, len(lines)
    in_code = False
    code_buf = []

    while i < n:
        line = lines[i]

        # 代码块 ```
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                code = "\n".join(code_buf)
                out.append(
                    '<pre style="background:#282c34;color:#abb2bf;padding:14px 16px;'
                    'border-radius:8px;overflow-x:auto;font-size:14px;line-height:1.6;'
                    f'margin:16px 0;"><code>{_escape(code)}</code></pre>'
                )
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            text = _inline(m.group(2), s)
            if level == 1:
                out.append(
                    f'<h1 style="font-size:22px;font-weight:700;color:{s["heading"]};'
                    f'margin:24px 0 12px;line-height:1.4;">{text}</h1>'
                )
            elif level == 2:
                out.append(
                    f'<h2 style="font-size:19px;font-weight:700;color:{s["heading"]};'
                    f'border-left:4px solid {s["accent"]};padding-left:10px;'
                    f'margin:28px 0 14px;line-height:1.4;">{text}</h2>'
                )
            else:
                size = {3: 17, 4: 16, 5: 15, 6: 14}[level]
                out.append(
                    f'<h{level} style="font-size:{size}px;font-weight:700;color:{s["heading"]};'
                    f'margin:22px 0 10px;line-height:1.4;">{text}</h{level}>'
                )
            i += 1
            continue

        # 分割线
        if re.match(r'^([-*_]\s*){3,}$', stripped):
            out.append(
                '<div style="text-align:center;margin:24px 0;">'
                f'<span style="display:inline-block;width:42px;height:3px;'
                f'background:{s["accent"]};border-radius:2px;"></span></div>'
            )
            i += 1
            continue

        # 引用
        if line.lstrip().startswith(">"):
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                buf.append(lines[i].lstrip()[1:].strip())
                i += 1
            text = _inline("<br>".join(buf), s)
            out.append(
                f'<blockquote style="background:{s["quote_bg"]};border-left:4px solid {s["accent"]};'
                'padding:14px 16px;margin:18px 0;border-radius:8px;color:#555;'
                f'font-size:15px;line-height:1.7;">{text}</blockquote>'
            )
            continue

        # 无序列表
        if re.match(r'^\s*[-*+]\s+', line):
            items = []
            while i < n and re.match(r'^\s*[-*+]\s+', lines[i]):
                items.append(_inline(re.sub(r'^\s*[-*+]\s+', '', lines[i]), s))
                i += 1
            lis = "".join(f'<li style="margin:6px 0;line-height:1.7;">{it}</li>' for it in items)
            out.append(f'<ul style="padding-left:24px;margin:12px 0;">{lis}</ul>')
            continue

        # 有序列表
        if re.match(r'^\s*\d+[.)]\s+', line):
            items = []
            while i < n and re.match(r'^\s*\d+[.)]\s+', lines[i]):
                items.append(_inline(re.sub(r'^\s*\d+[.)]\s+', '', lines[i]), s))
                i += 1
            lis = "".join(f'<li style="margin:6px 0;line-height:1.7;">{it}</li>' for it in items)
            out.append(f'<ol style="padding-left:24px;margin:12px 0;">{lis}</ol>')
            continue

        # 普通段落
        out.append(
            '<p style="font-size:16px;line-height:1.75;color:#333;margin:0 0 16px;">'
            f'{_inline(line, s)}</p>'
        )
        i += 1

    return "\n".join(out)


def render_full(title, md, theme="default"):
    """拼出带标题的完整正文 HTML（内联样式，可直接推草稿箱）。"""
    s = SCHEMES.get(theme, SCHEMES["default"])
    parts = [
        '<div style="font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\','
        "'Microsoft YaHei',sans-serif;color:#333;word-break:break-word;\">"
    ]
    if title:
        parts.append(
            f'<h1 style="font-size:24px;font-weight:700;color:{s["heading"]};'
            f'text-align:center;margin:16px 0 20px;line-height:1.4;">{_escape(title)}</h1>'
        )
    parts.append(markdown_to_html(md, theme))
    parts.append("</div>")
    return "".join(parts)
