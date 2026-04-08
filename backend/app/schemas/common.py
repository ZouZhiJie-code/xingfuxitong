from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int
    message: str
