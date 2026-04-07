from __future__ import annotations

from typing import Any

import httpx

from app.core.config import get_settings


def _extract_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(first.get("text"), str):
                return first["text"]

    if isinstance(payload.get("reply"), str):
        return payload["reply"]
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]

    return ""


def generate_reply(system_prompt: str, user_message: str) -> str:
    settings = get_settings()
    if not settings.minimax_api_key:
        return "当前未配置 MiniMax API Key，请联系管理员在后端环境变量中配置。"

    body = {
        "model": settings.minimax_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
    }
    headers = {"Authorization": f"Bearer {settings.minimax_api_key}", "Content-Type": "application/json"}

    try:
        response = httpx.post(
            settings.minimax_base_url,
            headers=headers,
            json=body,
            timeout=45.0,
        )
        response.raise_for_status()
        content = _extract_text(response.json())
        return content.strip() or "模型返回为空，请稍后重试。"
    except Exception:
        return "调用 MiniMax 模型失败，请稍后重试。"
