from app.core.config import get_settings
from app.services.llm_client import generate_reply


def test_unknown_provider_returns_hint(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "unknown")
    get_settings.cache_clear()
    assert "LLM_PROVIDER" in generate_reply("s", "u")
    get_settings.cache_clear()
