from fastapi import APIRouter

from .routes.project import router as project_router

api_router = APIRouter

api_router.include_router(project_router, prefix="/projects", tags=["Posts"])
