from app.core.config import get_settings
from app.services.minimax_client import generate_reply as minimax_generate_reply
from app.services.openai_client import generate_reply as openai_generate_reply


def generate_reply(system_prompt: str, user_message: str, history: list[dict[str, str]] | None = None, api_key_override: str | None = None) -> str:
    settings = get_settings()
    provider = settings.llm_provider.lower()

    if provider == "openai":
        return openai_generate_reply(system_prompt=system_prompt, user_message=user_message, history=history)

    if provider == "minimax":
        return minimax_generate_reply(system_prompt=system_prompt, user_message=user_message, api_key_override=api_key_override)

    return "未识别的 LLM_PROVIDER，请配置为 openai 或 minimax。"
