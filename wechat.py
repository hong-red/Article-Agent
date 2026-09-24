"""微信公众号草稿箱推送（可选功能，需自行配置 AppID / AppSecret）。"""
import os
import re
import time

import requests

# 清除代理环境变量，避免系统代理拦截微信 API（国内常见坑）
for _k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "api.weixin.qq.com,*.qq.com,qq.com,weixin.qq.com"
os.environ["no_proxy"] = "api.weixin.qq.com,*.qq.com,qq.com,weixin.qq.com"


class WeChatError(Exception):
    pass


# 常见错误码 → 友好提示
FRIENDLY = {
    "40164": "本机公网 IP 不在公众号「IP 白名单」里。请到 mp.weixin.qq.com → 设置与开发 → 基本配置 → IP白名单，把本机公网 IP 加进去。",
    "40013": "AppID 无效，请检查「设置」里填写的 AppID。",
    "40125": "AppSecret 无效，请检查「设置」里填写的 AppSecret。",
    "40001": "AppSecret 错误或 access_token 失效，请重新核对 AppSecret。",
    "41001": "缺少 access_token（通常是 AppSecret 错误）。",
    "48001": "公众号未认证或接口无权限（推送草稿需要「认证公众号」）。",
}


def _friendly(data):
    code = str(data.get("errcode", ""))
    hint = FRIENDLY.get(code, "")
    return f"errcode={code} errmsg={data.get('errmsg')}" + (f"（{hint}）" if hint else "")


def _is_public_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        a, b, c, d = (int(x) for x in parts)
    except ValueError:
        return False
    if a == 0 or a >= 224 or a == 10 or a == 127:
        return False
    if a == 172 and 16 <= b <= 31:
        return False
    if a == 192 and b == 168:
        return False
    return True


def get_public_ips():
    """探测本机公网出口 IP（可能有多个，供配置公众号 IP 白名单用）。"""
    # myip.ipip.net 与微信侧看到的来源 IP 一致，放最前面优先
    urls = [
        "https://myip.ipip.net",
        "http://ip.3322.net",
        "https://4.ipw.cn",
        "https://api.ipify.org",
    ]
    ips = []
    s = requests.Session()
    s.trust_env = False
    s.proxies = {"http": None, "https": None}
    for u in urls:
        try:
            r = s.get(u, timeout=8)
            if r.status_code == 200:
                m = re.search(r'(\d{1,3}\.){3}\d{1,3}', r.text)
                if m and _is_public_ip(m.group(0)) and m.group(0) not in ips:
                    ips.append(m.group(0))
        except requests.RequestException:
            continue
    return ips


_TOKEN = {"token": None, "expires_at": 0}


def get_access_token(appid, appsecret):
    if not appid or not appsecret:
        raise WeChatError("尚未配置公众号 AppID / AppSecret，请先在「设置」中填写。")

    # 命中缓存直接返回
    if _TOKEN["token"] and time.time() < _TOKEN["expires_at"] - 120:
        return _TOKEN["token"]

    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {"grant_type": "client_credential", "appid": appid, "secret": appsecret}
    try:
        resp = requests.get(url, params=params, timeout=30)
    except requests.RequestException as e:
        raise WeChatError(f"获取 access_token 失败：{e}")

    data = resp.json()
    if "access_token" not in data:
        raise WeChatError(f"获取 access_token 失败：{_friendly(data)}")

    _TOKEN["token"] = data["access_token"]
    _TOKEN["expires_at"] = time.time() + int(data.get("expires_in", 7200))
    return _TOKEN["token"]


def upload_thumb(appid, appsecret, file_path):
    """上传封面图为永久素材，返回 thumb_media_id。"""
    token = get_access_token(appid, appsecret)
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    with open(file_path, "rb") as f:
        files = {"media": (file_path.replace("\\", "/").rsplit("/", 1)[-1], f, "image/jpeg")}
        try:
            resp = requests.post(url, files=files, timeout=60)
        except requests.RequestException as e:
            raise WeChatError(f"上传封面图失败：{e}")

    data = resp.json()
    if "media_id" not in data:
        raise WeChatError(f"上传封面图失败：{_friendly(data)}")
    return data["media_id"]


def upload_image(appid, appsecret, file_path):
    """上传正文配图为永久素材，返回图片 url（用于正文 <img> 引用）。"""
    token = get_access_token(appid, appsecret)
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    with open(file_path, "rb") as f:
        files = {"media": (file_path.replace("\\", "/").rsplit("/", 1)[-1], f, "image/jpeg")}
        try:
            resp = requests.post(url, files=files, timeout=60)
        except requests.RequestException as e:
            raise WeChatError(f"上传正文配图失败：{e}")

    data = resp.json()
    if "url" not in data:
        raise WeChatError(f"上传正文配图失败：{_friendly(data)}")
    return data["url"]


def add_draft(appid, appsecret, article):
    """article: {title, author, digest, content, content_source_url, thumb_media_id, ...}"""
    if not article.get("thumb_media_id"):
        raise WeChatError("缺少封面图 thumb_media_id，请先上传封面图。")

    token = get_access_token(appid, appsecret)
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    payload = {"articles": [article]}
    try:
        resp = requests.post(url, json=payload, timeout=60)
    except requests.RequestException as e:
        raise WeChatError(f"推送草稿失败：{e}")

    data = resp.json()
    if data.get("errcode", 0) != 0:
        raise WeChatError(f"推送草稿失败：{_friendly(data)}")
    return data.get("media_id")
