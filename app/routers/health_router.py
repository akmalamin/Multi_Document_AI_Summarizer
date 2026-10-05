from fastapi import APIRouter, status
from datetime import datetime, timezone
from config import settings

router = APIRouter(tags=["System Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "engine_mode": "mock_offline" if settings.is_mock_mode else "live_openai",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }