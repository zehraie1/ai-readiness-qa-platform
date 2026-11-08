from fastapi import APIRouter

from app.modules.attempts.router import router as attempts_router
from app.modules.auth.router import router as auth_router
from app.modules.content.admin_router import router as admin_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.tracks.router import router as tracks_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(tracks_router)
api_router.include_router(attempts_router)
api_router.include_router(admin_router)
api_router.include_router(dashboard_router)
