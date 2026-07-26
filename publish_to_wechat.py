"""
微信公众号草稿箱自动推送脚本
- 处理秀米风格 HTML 文章
- 自动提取内联 CSS、图片
- 上传图片到微信素材库
- 创建草稿箱文章
"""
import os
import re
import sys
import json
import requests
import urllib3
from io import BytesIO
from dotenv import load_dotenv
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 强制清除代理环境变量（避免系统代理拦截微信 API）
for _key in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(_key, None)

# 设置 no_proxy 包含微信 API 域名
os.environ["NO_PROXY"] = "api.weixin.qq.com,*.qq.com,qq.com,weixin.qq.com"
os.environ["no_proxy"] = "api.weixin.qq.com,*.qq.com,qq.com,weixin.qq.com"

load_dotenv(override=True)


class WeChatDraftPublisher:
    """微信公众号草稿箱发布器"""

    def __init__(self):
        self.app_id = os.getenv("WECHAT_APP_ID")
        self.app_secret = os.getenv("WECHAT_APP_SECRET")
        if not self.app_id or not self.app_secret:
            raise ValueError(
                "请在 .env 文件中配置 WECHAT_APP_ID 和 WECHAT_APP_SECRET"
            )
        # 微信公众号 API 域名直连，不走代理
        self.client = WeChatClient(self.app_id, self.app_secret)
        # 显式禁用 wechatpy 内部 requests 使用的代理
        try:
            self.client.session.trust_env = False
            self.client.session.proxies = {"http": None, "https": None}
        except Exception:
            pass
        print(f"✅ 已连接微信公众号: {self.app_id}")

    def extract_inline_styles(self, html_content):
        """提取并内联化 CSS，将 <style> 中的样式应用到 HTML 元素"""
        # 提取 <style> 块
        style_match = re.search(r"<style[^>]*>(.*?)</style>", html_content, re.DOTALL)
        if not style_match:
            return html_content
        css_block = style_match.group(1)
        # 简单内联化（提取通用样式到 article 容器）
        article_style_rules = []
        for rule in re.findall(r"([^{]+)\{([^}]+)\}", css_block):
            selector, properties = rule
            selector = selector.strip()
            # 只对 article 内的元素生效
            if selector.startswith(".") or selector.startswith("#") or selector in ["body", "html"]:
                article_style_rules.append(f"{selector} {{{properties}}}")
        # 移除原始 <style> 块，在 article 容器前注入提取的样式
        html_content = re.sub(r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL)
        style_tag = "<style>" + "\n".join(article_style_rules) + "</style>"
        # 将 style 插入到 </head> 之前
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", f"{style_tag}\n</head>")
        else:
            html_content = style_tag + html_content
        return html_content

    def upload_content_image(self, image_path):
        """上传正文图片到微信（返回 URL，可直接在 <img> 中使用）"""
        if not os.path.exists(image_path):
            print(f"   ⚠️ 图片不存在: {image_path}")
            return None
        try:
            print(f"   📤 上传正文图片: {os.path.basename(image_path)}")
            with open(image_path, "rb") as f:
                img_bytes = BytesIO(f.read())
            # 使用 uploadimg 接口（专门用于图文消息内的图片）
            res = self.client.post(
                "media/uploadimg",
                files={"media": (os.path.basename(image_path), img_bytes, "image/jpeg")},
            )
            if isinstance(res, dict) and "url" in res:
                print(f"   ✅ 正文图片上传成功")
                return res["url"]
            print(f"   ⚠️ 上传返回异常: {res}")
            return None
        except WeChatClientException as e:
            print(f"   ❌ 正文图片上传失败: {e}")
            if "40164" in str(e):
                print("      💡 请将本机 IP (1.203.88.15) 加入微信公众号 IP 白名单")
            return None
        except Exception as e:
            print(f"   ❌ 上传异常: {e}")
            return None

    def upload_cover_image(self, image_path):
        """上传封面图到永久素材库"""
        if not os.path.exists(image_path):
            print(f"   ⚠️ 封面图不存在: {image_path}")
            return None
        try:
            print(f"   📸 上传封面图: {os.path.basename(image_path)}")
            with open(image_path, "rb") as f:
                result = self.client.material.add(
                    "image", (os.path.basename(image_path), f, "image/jpeg")
                )
            print(f"   ✅ 封面上传成功，media_id 已获取")
            return result["media_id"]
        except WeChatClientException as e:
            print(f"   ❌ 封面上传失败: {e}")
            if "40164" in str(e):
                print("      💡 请将本机 IP 加入微信公众号 IP 白名单")
            return None
        except Exception as e:
            print(f"   ❌ 上传异常: {e}")
            return None

    def process_html_images(self, html_content, article_folder):
        """处理 HTML 中所有本地相对路径图片，上传并替换为微信 URL"""
        pattern = re.compile(
            r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE
        )

        # 提取 body 内容
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html_content, re.DOTALL)
        body_content = body_match.group(1) if body_match else html_content

        image_urls = re.findall(r'src=["\']([^"\']+)["\']', body_content)
        local_images = [
            src for src in image_urls if not src.startswith(("http://", "https://", "data:"))
        ]
        print(f"🖼️  检测到 {len(local_images)} 张本地图片，开始上传...")

        uploaded = 0
        for src in set(local_images):
            img_path = os.path.join(article_folder, src)
            wechat_url = self.upload_content_image(img_path)
            if wechat_url:
                # 替换 HTML 中的路径（处理可能的引号差异）
                body_content = body_content.replace(f'src="{src}"', f'src="{wechat_url}"')
                body_content = body_content.replace(f"src='{src}'", f"src='{wechat_url}'")
                uploaded += 1
        print(f"✅ 成功上传 {uploaded}/{len(set(local_images))} 张图片")
        return body_content

    def create_draft(self, title, body_content, thumb_media_id, author="", digest=""):
        """创建草稿箱文章"""
        # 微信公众号文章 content 字段要求是图文消息内容
        # 必须在 <body> 之前有 <section> 等根标签
        article_html = f'<section style="max-width:100%;">{body_content}</section>'

        articles = [
            {
                "title": title,
                "author": author,
                "digest": digest[:120] if digest else "",
                "content": article_html,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
        try:
            print(f"📤 正在创建草稿箱文章...")
            # 使用 wechatpy draft API
            result = self.client.post("draft/add", data={"articles": articles})
            print(f"📋 草稿箱返回: {result}")
            if isinstance(result, dict):
                return result.get("media_id") or result.get("errcode", -1)
            return result
        except WeChatClientException as e:
            print(f"❌ 创建草稿失败: {e}")
            return None
        except Exception as e:
            print(f"❌ 创建草稿异常: {e}")
            return None


def publish_html_to_wechat(html_path, meta_path):
    """主流程：读取 HTML + meta，推送到微信草稿箱"""
    if not os.path.exists(html_path):
        print(f"❌ HTML 文件不存在: {html_path}")
        return
    if not os.path.exists(meta_path):
        print(f"❌ meta.json 不存在: {meta_path}")
        return

    # 读取 meta
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    title = meta.get("topic", "未命名文章")
    author = meta.get("author", "")
    digest = meta.get("abstract", "")
    cover_image = meta.get("cover_image", "default_cover.jpg")

    article_folder = os.path.dirname(html_path)

    # 读取 HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(f"\n{'='*60}")
    print(f"🚀 开始推送文章到微信草稿箱")
    print(f"   标题: {title}")
    print(f"   作者: {author}")
    print(f"   文件: {html_path}")
    print(f"{'='*60}\n")

    publisher = WeChatDraftPublisher()

    # 1. 上传封面
    print(f"📌 步骤 1/3：处理封面图")
    cover_path = os.path.join(article_folder, cover_image)
    if not os.path.exists(cover_path):
        # 尝试默认封面
        cover_path = os.path.join(article_folder, "default_cover.jpg")
    if not os.path.exists(cover_path):
        cover_path = os.path.join(os.path.dirname(article_folder), "default_cover.jpg")
    thumb_media_id = publisher.upload_cover_image(cover_path)
    if not thumb_media_id:
        print("❌ 封面上传失败，中止推送")
        return

    # 2. 处理正文
    print(f"\n📌 步骤 2/3：处理正文内容")
    body_content = publisher.process_html_images(html_content, article_folder)

    # 3. 创建草稿
    print(f"\n📌 步骤 3/3：创建草稿箱文章")
    media_id = publisher.create_draft(
        title=title,
        body_content=body_content,
        thumb_media_id=thumb_media_id,
        author=author,
        digest=digest,
    )

    if media_id and str(media_id) not in ["-1", "0"]:
        print(f"\n{'='*60}")
        print(f"🎉 推送成功！")
        print(f"   草稿 media_id: {media_id}")
        print(f"   请登录 https://mp.weixin.qq.com 查看草稿箱")
        print(f"{'='*60}\n")
    else:
        print(f"\n❌ 推送失败，请检查上方错误信息")


if __name__ == "__main__":
    # 默认推送当前文章的秀米版 HTML
    base = os.path.dirname(os.path.abspath(__file__))
    default_html = os.path.join(base, "articles", "shuzhiyuyun", "wechat_article.html")
    default_meta = os.path.join(base, "articles", "shuzhiyuyun", "meta.json")

    if len(sys.argv) >= 3:
        html_path = sys.argv[1]
        meta_path = sys.argv[2]
    else:
        html_path = default_html
        meta_path = default_meta

    publish_html_to_wechat(html_path, meta_path)
