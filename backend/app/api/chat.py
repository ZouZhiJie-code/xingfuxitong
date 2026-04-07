from collections.abc import Generator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, SessionStateResponse
from app.services.chat_session import (
    advance_element,
    append_assistant_message,
    append_user_message,
    get_or_create_session,
    get_recent_history,
)
from app.services.element_flow import ELEMENTS
from app.services.llm_client import generate_reply

router = APIRouter(prefix="/chat", tags=["chat"])


def _is_objective_fact(message: str) -> bool:
    text = message.strip()
    has_action = any(k in text for k in ["做", "完成", "学习", "工作", "跑", "写", "读", "练", "沟通", "运动"])
    return len(text) >= 8 and has_action


def _build_system_prompt(current_element: str, should_advance: bool) -> str:
    if should_advance:
        return (
            "你是幸福设计系统的教练型 AI。"
            f"用户当前刚完成“{current_element}”维度复盘。"
            "请理解用户语义后给出1句具体反馈，并引导进入下一个维度。"
            "语言自然，不要模板化。"
        )

    return (
        "你是幸福设计系统的教练型 AI。"
        f"用户正在“{current_element}”维度复盘。"
        "如果输入不够客观，请追问动作、时长、结果；"
        "若用户在问模型或系统能力，请先简短回答，再拉回复盘任务。"
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
    system_prompt = _build_system_prompt(current_element=current_element, should_advance=should_advance)
    assistant_reply = generate_reply(
        system_prompt=system_prompt,
        user_message=payload.message,
        history=get_recent_history(state),
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
