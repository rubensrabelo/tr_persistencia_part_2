from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from starlette import status

from models import Project
from database import get_session

router = APIRouter()


@router.post("/", response_model=Project)
async def create(project: Project,
                 session: Session = Depends(get_session)) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/", response_model=list[Project])
async def find_all(skip: int = 0, limit: int = 10,
                   session: Session = Depends(get_session)) -> list[Project]:
    projects = session.exec(select(Project).offset(skip).limit(limit)).all
    return projects


@router.get("/{project_id}", response_model=Project)
async def find_by_id(project_id: int,
                     session: Session = Depends(get_session)) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    return project


@router.put("/{project_id}", response_model=Project)
async def update(project_id: int, update_project: Project,
                 session: Session = Depends(get_session)) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    for key, value in update_project.dict(exclude_unset=True).items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}", response_model=Project)
async def delete(project_id: int,
                 session: Session = Depends(get_session)) -> dict:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    session.delete(project)
    session.commit()
    return {"message": "Project successfully deleted."}
