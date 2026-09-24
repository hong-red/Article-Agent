"""本地库：SQLite 存文章记录，正文另存 Markdown/HTML 文件。"""
import json
import os
import sqlite3
from datetime import datetime

import config


def _conn():
    config.ensure_dirs()
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                title TEXT,
                content_md TEXT,
                content_html TEXT,
                cover TEXT,
                theme TEXT DEFAULT 'default',
                status TEXT DEFAULT 'draft',
                created_at TEXT,
                updated_at TEXT
            )
            """
        )


def _now():
    return datetime.now().isoformat(timespec="seconds")


def insert_article(topic, title, content_md, content_html, cover="", theme="default"):
    now = _now()
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO articles (topic, title, content_md, content_html, cover, theme, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (topic, title, content_md, content_html, cover, theme, now, now),
        )
        return cur.lastrowid


def list_articles():
    with _conn() as conn:
        rows = conn.execute(
            "SELECT id, topic, title, theme, status, created_at, updated_at "
            "FROM articles ORDER BY updated_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_article(article_id):
    with _conn() as conn:
        row = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
    return dict(row) if row else None


def update_article(article_id, **fields):
    allowed = {"topic", "title", "content_md", "content_html", "cover", "theme", "status"}
    fields = {k: v for k, v in fields.items() if k in allowed}
    if not fields:
        return
    fields["updated_at"] = _now()
    sets = ", ".join(f"{k} = ?" for k in fields)
    vals = list(fields.values()) + [article_id]
    with _conn() as conn:
        conn.execute(f"UPDATE articles SET {sets} WHERE id = ?", vals)


def delete_article(article_id):
    with _conn() as conn:
        conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    # 同时删除封面文件
    cover_dir = os.path.join(config.ARTICLES_DIR, str(article_id))
    if os.path.isdir(cover_dir):
        for f in os.listdir(cover_dir):
            try:
                os.remove(os.path.join(cover_dir, f))
            except OSError:
                pass
        try:
            os.rmdir(cover_dir)
        except OSError:
            pass
