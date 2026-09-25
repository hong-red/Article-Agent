"""配置管理：本地 data/config.json 保存用户设置（API Key、公众号凭据等）。"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTICLES_DIR = os.path.join(DATA_DIR, "articles")
MATERIALS_DIR = os.path.join(DATA_DIR, "materials")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
DB_PATH = os.path.join(DATA_DIR, "articles.db")

DEFAULT_CONFIG = {
    "deepseek_api_key": "",
    "deepseek_model": "deepseek-chat",          # deepseek-chat / deepseek-reasoner
    "deepseek_base_url": "https://api.deepseek.com",
    "wechat_appid": "",
    "wechat_appsecret": "",
    # 公众号作者名 / 原文链接，推送草稿时使用
    "wechat_author": "",
    "wechat_source_url": "",
    # 是否开启评论
    "wechat_need_open_comment": 0,
    "wechat_only_fans_can_comment": 0,
    # 访问口令：设置后，所有 /api/* 请求需带 X-Access-Password 头（简单鉴权，防止陌生人访问）
    "access_password": "",
}


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    os.makedirs(MATERIALS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)


def load_config():
    ensure_dirs()
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save_config(updates):
    ensure_dirs()
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(updates)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return cfg
