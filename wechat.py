"""微信公众号草稿箱推送（可选功能，需自行配置 AppID / AppSecret）。"""
import os
import time

import requests

# 清除代理环境变量，避免系统代理拦截微信 API（国内常见坑）
for _k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "api.weixin.qq.com,*.qq.com,qq.com,weixin.qq.com"
os.environ["no_proxy"] = "api.weixin.qq.com,*.qq.com,qq.com,weixin.qq.com"


class WeChatError(Exception):
    pass


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
        raise WeChatError(f"获取 access_token 失败：errcode={data.get('errcode')} errmsg={data.get('errmsg')}")

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
        raise WeChatError(f"上传封面图失败：errcode={data.get('errcode')} errmsg={data.get('errmsg')}")
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
        raise WeChatError(f"上传正文配图失败：errcode={data.get('errcode')} errmsg={data.get('errmsg')}")
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
        raise WeChatError(f"推送草稿失败：errcode={data.get('errcode')} errmsg={data.get('errmsg')}")
    return data.get("media_id")
