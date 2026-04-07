from collections.abc import Generator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, SessionStateResponse
from app.services.chat_session import (
    advance_element,
    append_assistant_message,
    append_user_message,
    get_or_create_session,
)
from app.services.element_flow import ELEMENTS

router = APIRouter(prefix="/chat", tags=["chat"])


def _is_objective_fact(message: str) -> bool:
    return len(message.strip()) >= 8


def _build_assistant_reply(current_element: str, user_message: str, should_advance: bool) -> str:
    if not should_advance:
        return (
            f"我收到你在“{current_element}”维度的输入：{user_message}。"
            "请补充一个更具体的客观行为（例如做了什么、持续多久、结果如何）。"
        )

    return (
        f"已记录“{current_element}”维度行为事实：{user_message}。"
        "很好，我们继续下一个维度。"
    )


def _stream_text(text: str) -> Generator[str, None, None]:
    chunk_size = 18
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/stream")
def stream_chat(payload: ChatRequest) -> StreamingResponse:
    state = get_or_create_session(user_id=payload.user_id, session_id=payload.session_id)
    current_element = state.current_element
    append_user_message(state=state, message=payload.message)

    should_advance = _is_objective_fact(payload.message)
    assistant_reply = _build_assistant_reply(
        current_element=current_element,
        user_message=payload.message,
        should_advance=should_advance,
    )

    append_assistant_message(state=state, message=assistant_reply)
    if should_advance:
        advance_element(state)

    return StreamingResponse(_stream_text(assistant_reply), media_type="text/event-stream")


@router.get("/session/{user_id}/{session_id}")
def get_session_state(user_id: str, session_id: str) -> SessionStateResponse:
    state = get_or_create_session(user_id=user_id, session_id=session_id)
    return SessionStateResponse(
        user_id=state.user_id,
        session_id=state.session_id,
        current_element=state.current_element,
        completed_elements=ELEMENTS[: state.current_element_index],
        pending_elements=ELEMENTS[state.current_element_index :],
        total_messages=len(state.messages),
    )
