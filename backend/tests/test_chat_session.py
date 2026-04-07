from app.services.chat_session import advance_element, get_or_create_session


def test_session_created_with_first_element() -> None:
    state = get_or_create_session(user_id="u1", session_id="s1")
    assert state.current_element == "意义"


def test_advance_element_changes_state() -> None:
    state = get_or_create_session(user_id="u2", session_id="s2")
    advance_element(state)
    assert state.current_element == "意志"
