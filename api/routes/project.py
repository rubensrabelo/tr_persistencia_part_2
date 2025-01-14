from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from starlette import status

from models.project import Project, ProjectWithTask
from database import get_session

router = APIRouter()


@router.post("/", response_model=Project)
async def create_project(project: Project,
                         session: Session = Depends(get_session)) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/", response_model=list[ProjectWithTask])
async def find_all_project(offset: int = Query(default=0, ge=0),
                           limit: int = Query(default=10, le=100),
                           session: Session = Depends(get_session)
                           ) -> list[ProjectWithTask]:
    statement = (select(Project).offset(offset).limit(limit)
                 .options(joinedload(Project.tasks)))
    projects = session.exec(statement).unique().all()
    return projects


@router.get("/{project_id}", response_model=ProjectWithTask)
async def find_project_by_id(project_id: int,
                             session: Session = Depends(get_session)
                             ) -> ProjectWithTask:
    statement = (select(Project).where(Project.id == project_id)
                 .options(joinedload(Project.task)))
    project = session.exec(statement).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    return project


@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: int, update_project: Project,
                         session: Session = Depends(get_session)) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    for key, value in update_project.model_dump().items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}", response_model=Project)
async def delete_project(project_id: int,
                         session: Session = Depends(get_session)) -> dict:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    session.delete(project)
    session.commit()
    return {"Message": "Project successfully deleted."}


# Tasks
@router.post()
async def create_task():
    ...


@router.get()
async def find_all_task_by_post_id():
    ...


@router.get()
async def find_task_by_id():
    ...


@router.put()
async def update_task():
    ...


@router.delete
async def delete_task():
    ...
