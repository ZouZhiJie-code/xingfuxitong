from app.services.key_store import delete_minimax_key, get_minimax_key, save_minimax_key


def test_key_store_roundtrip() -> None:
    save_minimax_key("u-key", "sk-test-123")
    assert get_minimax_key("u-key") == "sk-test-123"
    delete_minimax_key("u-key")
    assert get_minimax_key("u-key") is None
