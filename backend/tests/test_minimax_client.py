from app.services.minimax_client import _extract_error, _extract_text


def test_extract_text_from_openai_style_choice() -> None:
    payload = {"choices": [{"message": {"content": "hello"}}]}
    assert _extract_text(payload) == "hello"


def test_extract_text_from_reply_field() -> None:
    payload = {"reply": "world"}
    assert _extract_text(payload) == "world"


def test_extract_error_message() -> None:
    payload = {"base_resp": {"status_code": 2049, "status_msg": "invalid api key"}}
    assert "invalid api key" in _extract_error(payload)
