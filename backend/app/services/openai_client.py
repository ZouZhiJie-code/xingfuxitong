from __future__ import annotations

from typing import Any

import httpx

from app.core.config import get_settings


def _extract_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""

    first = choices[0]
    if not isinstance(first, dict):
        return ""

    message = first.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts: list[str] = []
            for item in content:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    texts.append(item["text"])
            return "\n".join(texts)

    return ""


def generate_reply(system_prompt: str, user_message: str, history: list[dict[str, str]] | None = None) -> str:
    settings = get_settings()
    if not settings.openai_api_key:
        return "当前未配置 OpenAI API Key，请联系管理员在后端环境变量中配置。"

    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    for msg in history or []:
        role = msg.get("role")
        content = msg.get("content")
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_message})

    body = {
        "model": settings.openai_model,
        "messages": messages,
        "temperature": 0.2,
    }
    headers = {"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"}

    try:
        response = httpx.post(
            settings.openai_base_url,
            headers=headers,
            json=body,
            timeout=45.0,
        )
        response.raise_for_status()
        content = _extract_text(response.json())
        return content.strip() or "模型返回为空，请稍后重试。"
    except httpx.HTTPStatusError as exc:
        return f"模型调用失败（HTTP {exc.response.status_code}），请检查模型配置或密钥。"
    except Exception:
        return "调用 OpenAI 模型失败，请稍后重试。"
