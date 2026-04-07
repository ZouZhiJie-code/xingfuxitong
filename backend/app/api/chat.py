from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.element_flow import next_element

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/stream")
def stream_chat(payload: ChatRequest) -> StreamingResponse:
    target = next_element(None)

    def event_stream() -> str:
        chunks = [
            f"正在复盘维度：{target}。\n",
            f"收到你的输入：{payload.message}\n",
            "请继续补充一个客观行为事实。\n",
        ]
        for chunk in chunks:
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
