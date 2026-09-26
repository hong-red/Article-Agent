"""妙文 · 公众号文章自动生成器 —— FastAPI 后端。

三步生成：
  ① 主题 -> 生成题目 -> 选择
  ② 题目 -> 生成正文 -> 可反复调试
  ③ 正文 -> 格式优化 + 自定义美化 -> 预览
可选：推送到个人公众号草稿箱（需自行配置 AppID / AppSecret）。
"""
import os
import re
import time

from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
import db
import imagesearch
import llm
import markdown_html as mh
import wechat

app = FastAPI(title="妙文 · 公众号文章生成器")

# 允许跨域，方便以后 APP / 其他前端调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 简单访问口令：配置里设置了 access_password 后，所有 /api/* 请求需带 X-Access-Password 头
@app.middleware("http")
async def access_password_middleware(request: Request, call_next):
    path = request.url.path
    if path.startswith("/api/") and path != "/api/health":
        pw = (config.load_config().get("access_password") or "").strip()
        if pw and request.headers.get("x-access-password") != pw:
            return JSONResponse({"detail": "需要访问口令（X-Access-Password）"}, status_code=401)
    return await call_next(request)

config.ensure_dirs()
db.init_db()

BASE_DIR = config.BASE_DIR
STATIC_DIR = os.path.join(BASE_DIR, "static")
DEFAULT_COVER = os.path.join(BASE_DIR, "default_cover.jpg")
IMAGES_DIR = config.IMAGES_DIR


# ---------------- 请求模型 ----------------
class TitleReq(BaseModel):
    topic: str
    count: int = 5
    style: str = ""
    extra: str = ""
    template: str = "general"


class ContentReq(BaseModel):
    topic: str
    title: str
    style: str = ""
    extra: str = ""
    feedback: str = ""
    previous_content: str = ""
    template: str = "general"
    material_ids: list = []
    material_note: str = ""


class FormatReq(BaseModel):
    content: str
    title: str = ""
    theme: str = "default"
    tone: str = ""
    add_summary: bool = False
    add_golden: bool = False
    add_follow: bool = False
    polish: bool = True
    template: str = "general"
    images: list = []  # [{url, alt}] 待插入正文的配图


class RenderReq(BaseModel):
    content: str
    title: str = ""
    theme: str = "default"


class ArticleReq(BaseModel):
    topic: str
    title: str
    content_md: str
    content_html: str = ""
    cover: str = ""
    theme: str = "default"


# ---------------- 爆款写作模板 ----------------
TEMPLATES = {
    "general": {"name": "通用", "title": "", "content": "", "format": ""},
    "listicle": {
        "name": "干货清单型",
        "title": "标题突出「数字 + 实用价值」，如「5 个方法」「一篇讲透」，制造收藏欲。",
        "content": "用「总-分」结构：开头快速点出痛点/收益；主体用 ## 分点，每点一个小标题 + 说明 + 例子；结尾给行动建议。多用加粗和列表。",
        "format": "小标题带序号感，重点结论加粗，关键处用引用块强调。",
    },
    "hook": {
        "name": "悬念钩子型",
        "title": "标题制造强烈好奇心或反差，如「为什么…」「…的真相」，让人忍不住点开。",
        "content": "开头 1~2 句抛悬念或反常识结论，正文层层揭晓，结尾收束点题。多用短句、留白。",
        "format": "开头悬念句单独成段或加粗，段落短、节奏快。",
    },
    "emotion": {
        "name": "情感共鸣型",
        "title": "标题带情绪和代入感，如「多少人…」「原来…」，让读者觉得说的是自己。",
        "content": "用一个真实感强的故事或场景开头，中间引发共鸣，结尾升华情绪并引导转发。语言温暖、有画面感。",
        "format": "金句单独成段并加粗，营造情绪节奏。",
    },
    "opinion": {
        "name": "热点观点型",
        "title": "标题带鲜明观点或冲突，如「…才是最…」「别再说…了」。",
        "content": "开头亮出犀利观点，主体摆事实讲道理、分点论证，结尾给有力结论。逻辑清晰、金句频出。",
        "format": "核心观点用引用块或加粗突出，金句醒目。",
    },
    "story": {
        "name": "故事叙事型",
        "title": "标题有故事感和画面感，如「那个…的人，后来…」。",
        "content": "以具体人物/事件的故事线展开，有起承转合，结尾回扣主题或留余味。多用细节描写。",
        "format": "段落自然连贯，关键转折可加粗，营造叙事节奏。",
    },
}


# ---------------- 工具 ----------------
def _cfg():
    return config.load_config()


def _llm(messages, temperature=0.8, max_tokens=4096):
    c = _cfg()
    return llm.chat(
        messages,
        c["deepseek_api_key"],
        model=c["deepseek_model"],
        base_url=c["deepseek_base_url"],
        temperature=temperature,
        max_tokens=max_tokens,
    )


def _truncate_bytes(s, max_bytes):
    """按 UTF-8 字节数截断，不切碎多字节字符（中文 1 字 = 3 字节）。"""
    b = s.encode("utf-8")
    if len(b) <= max_bytes:
        return s
    out, total = [], 0
    for ch in s:
        bl = len(ch.encode("utf-8"))
        if total + bl > max_bytes:
            break
        out.append(ch)
        total += bl
    return "".join(out)


def _plain_digest(md, max_bytes=120):
    """从正文生成摘要，按字节截到微信 description 上限（120 字节 ≈ 40 汉字）。"""
    text = re.sub(r'[#>*`\-]', '', md)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return _truncate_bytes(text, max_bytes)


def _cover_url(article):
    cover = article.get("cover") or ""
    if cover and os.path.exists(cover):
        name = os.path.basename(cover)
        return f"/files/{article['id']}/{name}"
    return ""


def _write_article_files(article_id, md, html):
    d = os.path.join(config.ARTICLES_DIR, str(article_id))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "article.md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(d, "article.html"), "w", encoding="utf-8") as f:
        f.write(html)


# ---------------- 基础 ----------------
@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/config")
def get_config():
    return _cfg()


@app.post("/api/config")
def set_config(body: dict):
    return config.save_config(body)


@app.get("/api/themes")
def themes():
    return mh.list_schemes()


@app.get("/api/templates")
def templates():
    return [{"key": k, "name": v["name"]} for k, v in TEMPLATES.items()]


@app.post("/api/test/llm")
def test_llm():
    try:
        reply = _llm([{"role": "user", "content": "请只回复两个字：正常"}], max_tokens=16)
        return {"ok": True, "reply": reply}
    except llm.LLMError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/wechat/ip")
def wechat_ip():
    return {"ips": wechat.get_public_ips()}


# ---------------- 第 1 步：生成题目 ----------------
@app.post("/api/generate/titles")
def generate_titles(req: TitleReq):
    style_line = f"风格倾向：{req.style}" if req.style else ""
    extra_line = f"补充说明：{req.extra}" if req.extra else ""
    tpl = TEMPLATES.get(req.template, TEMPLATES["general"])
    tpl_line = f"标题风格：{tpl['title']}" if tpl["title"] else ""
    user = (
        f"请为主题「{req.topic}」生成 {req.count} 个吸引人的公众号文章标题。\n"
        "要求：\n"
        "1. 有吸引力，包含悬念、利益点或情绪点\n"
        "2. 符合公众号调性，口语化但不低俗\n"
        "3. 每个标题 15~25 字\n"
        "4. 只输出标题，每行一个，不要编号、引号或解释\n"
        + (style_line + "\n" if style_line else "")
        + (extra_line + "\n" if extra_line else "")
        + (tpl_line + "\n" if tpl_line else "")
    )
    raw = _llm(
        [
            {"role": "system", "content": "你是资深公众号主编，擅长起标题。"},
            {"role": "user", "content": user},
        ],
        temperature=1.0,
        max_tokens=800,
    )

    titles = []
    for line in raw.split("\n"):
        t = line.strip()
        t = re.sub(r'^[\d\-\*\.、\)）\s]+', '', t).strip()
        t = t.strip('「」""\'\'“”')
        if t and t not in titles:
            titles.append(t)
    if not titles:
        titles = [raw.strip()]
    return {"titles": titles[: max(req.count, 1)]}


# ---------------- 第 2 步：生成正文 ----------------
@app.post("/api/generate/content")
def _read_material_text(material_id, limit=8000):
    """读取文本类素材内容供 AI 引用；图片/二进制返回 None。"""
    try:
        mid = int(material_id)
    except (TypeError, ValueError):
        return None
    m = db.get_material(mid)
    if not m or not m.get("path") or not os.path.exists(m["path"]):
        return None
    ext = os.path.splitext(m["path"])[1].lower()
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".zip", ".pdf", ".doc", ".docx"):
        return None
    try:
        with open(m["path"], "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception:
        return None
    text = (text or "").strip()
    if not text:
        return None
    return f"【素材《{m['name']}》】\n{text[:limit]}"


def generate_content(req: ContentReq):
    style_line = f"风格倾向：{req.style}" if req.style else ""
    extra_line = f"补充说明：{req.extra}" if req.extra else ""
    tpl = TEMPLATES.get(req.template, TEMPLATES["general"])
    tpl_line = f"写作模板：{tpl['content']}" if tpl["content"] else ""
    feedback_line = (
        f"【修改要求】{req.feedback}\n请在上面的要求基础上，重点满足这条修改要求。"
        if req.feedback else ""
    )
    previous_line = (
        f"【上一版内容】\n{req.previous_content}\n请基于这版内容修改，而不是完全重写。"
        if req.previous_content else ""
    )
    # 素材库：读取选中素材内容供 AI 引用
    mat_segs = []
    for mid in (req.material_ids or []):
        seg = _read_material_text(mid)
        if seg:
            mat_segs.append(seg)
    material_block = ""
    if mat_segs:
        note = f"优化要求：{req.material_note}\n" if (req.material_note or "").strip() else ""
        material_block = (
            "\n【参考资料/素材】请务必结合下面的素材内容来写，引用其中的关键信息、数据或观点。\n"
            + note + "\n\n".join(mat_segs) + "\n"
        )
    user = (
        f"请根据下面的题目和主题，写一篇结构完整、可读性强、可直接发布的公众号文章。\n\n"
        f"题目：{req.title}\n"
        f"主题：{req.topic}\n"
        + (style_line + "\n" if style_line else "")
        + (extra_line + "\n" if extra_line else "")
        + (tpl_line + "\n" if tpl_line else "")
        + "\n写作要求：\n"
        "1. 使用 Markdown 格式：小标题用 ##，适当使用列表、加粗、引用\n"
        "2. 有清晰的开头引入、主体分点、结尾总结\n"
        "3. 语言自然流畅，像真人写作，避免 AI 腔\n"
        "4. 篇幅适中（1000~1800 字）\n"
        + (material_block + "\n" if material_block else "")
        + (feedback_line + "\n" if feedback_line else "")
        + (previous_line + "\n" if previous_line else "")
    )
    content = _llm(
        [
            {"role": "system", "content": "你是资深公众号写作者，产出可直接发布的文章。"},
            {"role": "user", "content": user},
        ],
        temperature=0.8,
        max_tokens=4096,
    )
    return {"content": content.strip()}


# ---------------- 第 4 步：格式优化 ----------------
def _image_refs(images):
    """把前端传来的图片清单规范化成 [{url, alt}]。"""
    out = []
    for i in images or []:
        if isinstance(i, dict) and i.get("url"):
            out.append({
                "url": i["url"],
                "alt": (i.get("alt") or i.get("name") or "配图").strip() or "配图",
            })
    return out


def _ensure_images(md, images):
    """保证每张图都出现在正文里；缺失的补到末尾。"""
    for img in images:
        if img["url"] and img["url"] not in md:
            md = md.rstrip() + f"\n\n![{img['alt']}]({img['url']})"
    return md


@app.post("/api/generate/format")
def generate_format(req: FormatReq):
    tpl = TEMPLATES.get(req.template, TEMPLATES["general"])
    images = _image_refs(req.images)
    if req.polish:
        reqs = []
        if req.add_summary:
            reqs.append("- 在正文最前面加一段「导语/摘要」（不超过 60 字，用普通段落）")
        if req.add_golden:
            reqs.append("- 提炼 1~3 句金句，用加粗或引用块突出")
        if req.add_follow:
            reqs.append("- 在结尾加一段自然的「引导关注」语")
        if req.tone:
            reqs.append(f"- 整体语气调整为：{req.tone}")
        if tpl.get("format"):
            reqs.append(tpl["format"])
        if images:
            img_desc = "\n".join(f"{i + 1}. {img['alt']}：{img['url']}" for i, img in enumerate(images))
            reqs.append(
                "把下面的配图插入到正文中与内容最相关的位置（每张图放在相关段落/小节附近，"
                "用 Markdown 图片语法，图片地址必须原样保留、不得改动）：\n" + img_desc
            )
        if not reqs:
            reqs.append("- 优化小标题层级、段落节奏，让重点更突出")
        reqs.append("- 保持原意和事实不变，不新增虚假信息")
        user = (
            "请对下面的文章进行格式优化与润色，只输出优化后的 Markdown 正文，不要多余解释。\n"
            "优化要求：\n" + "\n".join(reqs) + "\n\n【原文】\n" + req.content
        )
        md = _llm(
            [
                {"role": "system", "content": "你是公众号排版专家，擅长把文章优化得更有层次、更易读。"},
                {"role": "user", "content": user},
            ],
            temperature=0.6,
            max_tokens=4096,
        ).strip()
    else:
        md = req.content

    md = _ensure_images(md, images)
    html = mh.render_full(req.title, md, req.theme)
    return {"content": md, "html": html}


# ---------------- 渲染（无 LLM，实时预览用） ----------------
@app.post("/api/render")
def render(req: RenderReq):
    return {"html": mh.render_full(req.title, req.content, req.theme)}


# ---------------- 本地库 CRUD ----------------
@app.get("/api/articles")
def list_articles():
    articles = db.list_articles()
    for a in articles:
        a["cover_url"] = _cover_url(db.get_article(a["id"]))
    return articles


@app.post("/api/articles")
def create_article(req: ArticleReq):
    html = req.content_html or mh.render_full(req.title, req.content_md, req.theme)
    article_id = db.insert_article(req.topic, req.title, req.content_md, html, req.cover, req.theme)
    _write_article_files(article_id, req.content_md, html)
    return {"id": article_id}


@app.get("/api/articles/{article_id}")
def get_article(article_id: int):
    a = db.get_article(article_id)
    if not a:
        raise HTTPException(status_code=404, detail="文章不存在")
    a["cover_url"] = _cover_url(a)
    return a


@app.put("/api/articles/{article_id}")
def update_article(article_id: int, req: ArticleReq):
    a = db.get_article(article_id)
    if not a:
        raise HTTPException(status_code=404, detail="文章不存在")
    html = req.content_html or mh.render_full(req.title, req.content_md, req.theme)
    db.update_article(
        article_id,
        topic=req.topic,
        title=req.title,
        content_md=req.content_md,
        content_html=html,
        cover=req.cover,
        theme=req.theme,
    )
    _write_article_files(article_id, req.content_md, html)
    return {"id": article_id}


@app.delete("/api/articles/{article_id}")
def delete_article(article_id: int):
    db.delete_article(article_id)
    return {"ok": True}


@app.post("/api/articles/{article_id}/cover")
async def upload_cover(article_id: int, file: UploadFile = File(...)):
    a = db.get_article(article_id)
    if not a:
        raise HTTPException(status_code=404, detail="文章不存在")
    ext = os.path.splitext(file.filename or "cover.jpg")[1].lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    d = os.path.join(config.ARTICLES_DIR, str(article_id))
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"cover{ext}")
    data = await file.read()
    with open(path, "wb") as f:
        f.write(data)
    db.update_article(article_id, cover=path)
    return {"ok": True, "cover_url": f"/files/{article_id}/cover{ext}"}


# ---------------- 推送草稿箱（可选） ----------------
_IMG_TAG_RE = re.compile(r'<img\s+[^>]*>')
_SRC_RE = re.compile(r'src="([^"]+)"')


def _resolve_wechat_images(appid, appsecret, html):
    """把正文里引用本地 /images/ 的 <img> 上传到微信永久素材，换成微信图片地址。"""
    def repl(tag):
        m = _SRC_RE.search(tag.group(0))
        if not m:
            return tag.group(0)
        src = m.group(1)
        name = os.path.basename(src.split("?")[0].rstrip("/"))
        local = os.path.join(IMAGES_DIR, name)
        if not os.path.exists(local):
            return tag.group(0)
        try:
            wechat_url = wechat.upload_image(appid, appsecret, local)
        except wechat.WeChatError:
            return tag.group(0)
        if not wechat_url:
            return tag.group(0)
        attrs = tag.group(0)
        if 'data-src="' in attrs:
            attrs = attrs.replace(m.group(0), f'src="{wechat_url}"')
        else:
            attrs = attrs.replace(m.group(0), f'data-src="{wechat_url}" src="{wechat_url}"')
        return attrs
    return _IMG_TAG_RE.sub(repl, html)


@app.post("/api/articles/{article_id}/push")
def push_draft(article_id: int):
    article = db.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    c = _cfg()

    cover = article.get("cover") or ""
    if not cover or not os.path.exists(cover):
        if os.path.exists(DEFAULT_COVER):
            cover = DEFAULT_COVER
        else:
            raise HTTPException(status_code=400, detail="缺少封面图，请先在第 4 步上传封面。")

    try:
        thumb = wechat.upload_thumb(c["wechat_appid"], c["wechat_appsecret"], cover)
        html = article["content_html"] or mh.render_full(
            article["title"], article["content_md"], article["theme"]
        )
        html = _resolve_wechat_images(c["wechat_appid"], c["wechat_appsecret"], html)
        draft = {
            "title": article["title"],
            "author": c.get("wechat_author", ""),
            "digest": _plain_digest(article["content_md"]),
            "content": html,
            "content_source_url": c.get("wechat_source_url", ""),
            "thumb_media_id": thumb,
            "need_open_comment": int(c.get("wechat_need_open_comment", 0) or 0),
            "only_fans_can_comment": int(c.get("wechat_only_fans_can_comment", 0) or 0),
        }
        media_id = wechat.add_draft(c["wechat_appid"], c["wechat_appsecret"], draft)
        db.update_article(article_id, status="pushed")
        return {"ok": True, "draft_media_id": media_id}
    except wechat.WeChatError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------- 素材库 ----------------
@app.get("/api/materials")
def list_materials():
    return db.list_materials()


@app.post("/api/materials")
async def upload_material(file: UploadFile = File(...)):
    name = os.path.basename(file.filename or "material.txt") or "material.txt"
    base, ext = os.path.splitext(name)
    path = os.path.join(config.MATERIALS_DIR, name)
    i = 1
    while os.path.exists(path):
        path = os.path.join(config.MATERIALS_DIR, f"{base}_{i}{ext}")
        i += 1
    data = await file.read()
    with open(path, "wb") as f:
        f.write(data)
    mid = db.insert_material(os.path.basename(path), path, len(data))
    return {"id": mid, "name": os.path.basename(path)}


@app.delete("/api/materials/{material_id}")
def delete_material(material_id: int):
    m = db.get_material(material_id)
    if m:
        p = m.get("path") or ""
        if p and os.path.exists(p):
            try:
                os.remove(p)
            except OSError:
                pass
        db.delete_material(material_id)
    return {"ok": True}


# ---------------- 图片库（选图步骤用） ----------------
class ImageSearchReq(BaseModel):
    query: str


class ImageFetchReq(BaseModel):
    url: str
    thumb: str = ""
    page: str = ""


def _safe_img_ext(ext):
    ext = (ext or "").lower()
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"):
        ext = ".jpg"
    return ext


def _unique_image_path(ext):
    config.ensure_dirs()
    base = f"img_{int(time.time() * 1000)}"
    path = os.path.join(IMAGES_DIR, f"{base}{ext}")
    i = 1
    while os.path.exists(path):
        path = os.path.join(IMAGES_DIR, f"{base}_{i}{ext}")
        i += 1
    return path


@app.get("/api/images")
def list_images():
    config.ensure_dirs()
    items = []
    for name in sorted(os.listdir(IMAGES_DIR)):
        if os.path.splitext(name)[1].lower() not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"):
            continue
        p = os.path.join(IMAGES_DIR, name)
        if os.path.isfile(p):
            items.append({"name": name, "url": f"/images/{name}", "size": os.path.getsize(p)})
    return items


@app.post("/api/images")
async def upload_images(files: list[UploadFile] = File(...)):
    config.ensure_dirs()
    out = []
    for file in files:
        name = os.path.basename(file.filename or "image.jpg") or "image.jpg"
        # 去掉空格等，避免 URL 里出问题
        name = re.sub(r'[\s　]+', '_', name)
        ext = _safe_img_ext(os.path.splitext(name)[1])
        base = os.path.splitext(name)[0] or "image"
        data = await file.read()
        if not data:
            continue
        path = os.path.join(IMAGES_DIR, f"{base}{ext}")
        i = 1
        while os.path.exists(path):
            path = os.path.join(IMAGES_DIR, f"{base}_{i}{ext}")
            i += 1
        with open(path, "wb") as f:
            f.write(data)
        final = os.path.basename(path)
        out.append({"name": final, "url": f"/images/{final}"})
    return out


@app.delete("/api/images/{name}")
def delete_image(name: str):
    name = os.path.basename(name)
    p = os.path.join(IMAGES_DIR, name)
    if os.path.isfile(p):
        try:
            os.remove(p)
        except OSError:
            pass
    return {"ok": True}


@app.post("/api/images/search")
def search_images(req: ImageSearchReq):
    try:
        return {"results": imagesearch.search(req.query)}
    except imagesearch.SearchError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/images/fetch")
def fetch_image(req: ImageFetchReq):
    config.ensure_dirs()
    candidates = [u for u in (req.url, req.thumb) if u]
    if not candidates:
        raise HTTPException(status_code=400, detail="缺少图片地址")
    last_err = None
    for u in candidates:
        try:
            data, ctype = imagesearch.download(u, referer=req.page)
            ext = imagesearch._ext_from_ctype(ctype)
            if not ext:
                ext = _safe_img_ext(os.path.splitext(u.split("?")[0])[1])
            path = _unique_image_path(ext)
            with open(path, "wb") as f:
                f.write(data)
            final = os.path.basename(path)
            return {"name": final, "url": f"/images/{final}"}
        except Exception as e:  # noqa: BLE001 —— 逐个候选尝试
            last_err = e
    raise HTTPException(status_code=400, detail=f"图片下载失败：{last_err or '未知错误'}")


# ---------------- 静态资源 ----------------
@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


app.mount("/files", StaticFiles(directory=config.ARTICLES_DIR), name="files")
app.mount("/materials", StaticFiles(directory=config.MATERIALS_DIR), name="materials")
app.mount("/images", StaticFiles(directory=config.IMAGES_DIR), name="images")
# 前端静态资源挂到根路径（style.css / app.js 等），放最后避免遮挡上面的 /api 与 /files 等；
# 这样 index.html 用相对路径 style.css，能同时兼容 GitHub Pages 和本服务
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
