from fastapi import APIRouter

from .routes.project import router as project_router
from .routes.collaborator import router as collaborator_router

api_router = APIRouter()

api_router.include_router(project_router, prefix="/projects", tags=["Posts"])
api_router.include_router(collaborator_router, prefix="/collaborator",
                          tags=["Collaborator"])
