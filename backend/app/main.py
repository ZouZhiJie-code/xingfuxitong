from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.journal import router as journal_router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)
origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
allow_credentials = "*" not in origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(chat_router, prefix="/api/v1")
app.include_router(journal_router, prefix="/api/v1")
