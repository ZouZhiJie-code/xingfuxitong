from fastapi import APIRouter

from app.schemas.key import KeyDeleteRequest, KeyStatusResponse, KeyUpsertRequest, KeyVerifyRequest
from app.services.key_store import delete_minimax_key, get_minimax_key, has_minimax_key, save_minimax_key
from app.services.minimax_client import generate_reply

router = APIRouter(prefix="/keys", tags=["keys"])


def _mask(api_key: str) -> str:
    if len(api_key) <= 8:
        return "*" * len(api_key)
    return f"{api_key[:4]}***{api_key[-4:]}"


@router.post("/minimax")
def upsert_minimax_key(payload: KeyUpsertRequest) -> KeyStatusResponse:
    save_minimax_key(user_id=payload.user_id, api_key=payload.api_key)
    return KeyStatusResponse(user_id=payload.user_id, has_key=True, key_masked=_mask(payload.api_key))


@router.post("/minimax/verify")
def verify_minimax_key(payload: KeyVerifyRequest) -> dict[str, str | bool]:
    api_key = get_minimax_key(user_id=payload.user_id)
    if not api_key:
        return {"ok": False, "message": "请先配置 MiniMax API Key"}

    probe = generate_reply(system_prompt="你是一个简短助手，只回复“OK”。", user_message="测试", api_key_override=api_key)
    ok = "invalid api key" not in probe.lower() and "未配置" not in probe
    return {"ok": ok, "message": probe}


@router.delete("/minimax")
def remove_minimax_key(payload: KeyDeleteRequest) -> dict[str, bool]:
    delete_minimax_key(user_id=payload.user_id)
    return {"ok": True}


@router.get("/minimax/{user_id}")
def minimax_key_status(user_id: str) -> KeyStatusResponse:
    key = get_minimax_key(user_id=user_id)
    if not key:
        return KeyStatusResponse(user_id=user_id, has_key=False)
    return KeyStatusResponse(user_id=user_id, has_key=has_minimax_key(user_id), key_masked=_mask(key))
