from pydantic import BaseModel, Field


class KeyUpsertRequest(BaseModel):
    user_id: str = Field(min_length=1)
    api_key: str = Field(min_length=1)


class KeyVerifyRequest(BaseModel):
    user_id: str = Field(min_length=1)


class KeyDeleteRequest(BaseModel):
    user_id: str = Field(min_length=1)


class KeyStatusResponse(BaseModel):
    user_id: str
    has_key: bool
    key_masked: str | None = None
