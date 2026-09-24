"""全网图片搜索 + 图片下载。

使用必应图片搜索（无需 API Key），国内网络可达。
返回结果里 `url` 为原图地址，`thumb` 为缩略图地址，`page` 为来源页面。
"""
import html as _html
import json
import re

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

IMG_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp")


class SearchError(Exception):
    pass


def _session():
    """直连（不走系统代理），国内访问必应更稳定。"""
    s = requests.Session()
    s.trust_env = False
    s.proxies = {"http": None, "https": None}
    return s


def _domain(u):
    m = re.match(r"https?://([^/]+)", u or "")
    return m.group(1) if m else ""


def search(query, count=30):
    """搜索图片，返回 [{url, thumb, title, source, page}]。"""
    q = (query or "").strip()
    if not q:
        return []

    url = "https://cn.bing.com/images/async"
    params = {"q": q, "first": 0, "count": max(1, min(int(count or 30), 60)), "mmasync": 1}
    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Referer": f"https://cn.bing.com/images/search?q={requests.utils.quote(q)}",
    }
    try:
        resp = _session().get(url, params=params, headers=headers, timeout=30)
    except requests.RequestException as e:
        raise SearchError(f"搜索失败：{e}")

    if resp.status_code != 200:
        raise SearchError(f"搜索失败：HTTP {resp.status_code}")

    results = []
    for m in re.finditer(r'm="([^"]*)"', resp.text):
        try:
            obj = json.loads(_html.unescape(m.group(1)))
        except (json.JSONDecodeError, ValueError):
            continue
        murl = obj.get("murl") or ""
        turl = obj.get("turl") or ""
        if not murl and not turl:
            continue
        results.append({
            "url": murl or turl,
            "thumb": turl or murl,
            "title": (obj.get("t") or obj.get("desc") or "").strip(),
            "source": _domain(obj.get("purl") or murl or turl),
            "page": obj.get("purl") or "",
        })

    seen, out = set(), []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            out.append(r)
    return out


def _ext_from_ctype(ctype):
    ctype = (ctype or "").lower()
    if "png" in ctype:
        return ".png"
    if "gif" in ctype:
        return ".gif"
    if "webp" in ctype:
        return ".webp"
    if "bmp" in ctype:
        return ".bmp"
    if "jpeg" in ctype or "jpg" in ctype:
        return ".jpg"
    return ""


def download(url, referer="", timeout=30):
    """下载图片字节，返回 (bytes, content_type)。"""
    headers = {"User-Agent": UA, "Accept": "image/*,*/*;q=0.8"}
    if referer:
        headers["Referer"] = referer
    r = _session().get(url, headers=headers, timeout=timeout, stream=True)
    r.raise_for_status()
    return r.content, r.headers.get("Content-Type", "")
