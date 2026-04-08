from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "assistant", "user"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class SessionStateResponse(BaseModel):
    user_id: str
    session_id: str
    current_element: str
    completed_elements: list[str]
    pending_elements: list[str]
    total_messages: int
