"""DeepSeek 客户端（OpenAI 兼容接口）。"""
import json
import requests


class LLMError(Exception):
    pass


def chat(messages, api_key, model="deepseek-chat",
         base_url="https://api.deepseek.com",
         temperature=0.8, max_tokens=4096):
    if not api_key:
        raise LLMError("尚未配置 DeepSeek API Key，请先点击右上角「设置」填写。")

    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=300)
    except requests.RequestException as e:
        raise LLMError(f"请求 DeepSeek 失败：{e}")

    if resp.status_code != 200:
        raise LLMError(f"DeepSeek 返回错误 {resp.status_code}：{resp.text[:500]}")

    try:
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError):
        raise LLMError(f"DeepSeek 响应解析失败：{resp.text[:500]}")
