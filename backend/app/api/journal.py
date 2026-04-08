from fastapi import APIRouter

router = APIRouter(prefix="/journals", tags=["journals"])


@router.get("/today")
def get_today_journal() -> dict[str, str | int]:
    return {"date": "today", "total_score": 0, "summary": "开发初始化阶段"}
