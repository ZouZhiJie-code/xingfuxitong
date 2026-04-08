from dataclasses import dataclass, field
from threading import Lock

from app.services.element_flow import ELEMENTS


@dataclass
class SessionState:
    user_id: str
    session_id: str
    current_element_index: int = 0
    messages: list[dict[str, str]] = field(default_factory=list)

    @property
    def current_element(self) -> str:
        return ELEMENTS[self.current_element_index]


_SESSION_STORE: dict[str, SessionState] = {}
_LOCK = Lock()


def _session_key(user_id: str, session_id: str) -> str:
    return f"{user_id}:{session_id}"


def get_or_create_session(user_id: str, session_id: str) -> SessionState:
    key = _session_key(user_id=user_id, session_id=session_id)
    with _LOCK:
        if key not in _SESSION_STORE:
            _SESSION_STORE[key] = SessionState(user_id=user_id, session_id=session_id)
        return _SESSION_STORE[key]


def append_user_message(state: SessionState, message: str) -> None:
    state.messages.append({"role": "user", "content": message, "element": state.current_element})


def append_assistant_message(state: SessionState, message: str) -> None:
    state.messages.append({"role": "assistant", "content": message, "element": state.current_element})


def advance_element(state: SessionState) -> None:
    if state.current_element_index < len(ELEMENTS) - 1:
        state.current_element_index += 1


def get_recent_history(state: SessionState, limit: int = 6) -> list[dict[str, str]]:
    return state.messages[-limit:]
