from app.services.element_flow import next_element


def test_next_element_default() -> None:
    assert next_element(None) == "意义"


def test_next_element_progress() -> None:
    assert next_element("健康") == "人际"
