from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.sql import func
from sqlalchemy import asc
from sqlalchemy.orm import joinedload
from starlette import status
from datetime import datetime, timezone

from database import get_session
from models.project import Project
from dto.project_dto import ProjecBaseWithTask

router = APIRouter()


# Project
@router.post("/",
             response_model=Project,
             status_code=status.HTTP_201_CREATED
             )
async def create_project(project: Project,
                         session: Session = Depends(get_session)) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


# Listar todos os projetos
@router.get("/",
            response_model=list[ProjecBaseWithTask],
            status_code=status.HTTP_200_OK
            )
async def find_all_project(offset: int = Query(default=0, ge=0),
                           limit: int = Query(default=10, le=100),
                           session: Session = Depends(get_session)
                           ) -> list[ProjecBaseWithTask]:
    statement = (
        select(Project)
        .offset(offset)
        .limit(limit)
        .order_by(asc(Project.created_at))
        .options(joinedload(Project.tasks))
        )
    projects = session.exec(statement).unique().all()
    return projects


# Mostrar um projeto por id
@router.get("/{project_id}",
            response_model=ProjecBaseWithTask,
            status_code=status.HTTP_200_OK
            )
async def find_project_by_id(project_id: int,
                             session: Session = Depends(get_session)
                             ) -> ProjecBaseWithTask:
    statement = (select(Project).where(Project.id == project_id)
                 .options(joinedload(Project.tasks)))
    project = session.exec(statement).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    return project


# Listar os títulos de projetos cujo título contém determinada string.
@router.get("/titles/name/search",
            response_model=list[str],
            status_code=status.HTTP_200_OK
            )
async def search_project_titles(name: str,
                                session: Session = Depends(get_session)
                                ) -> list[str]:
    statement = select(Project.name).where(
        Project.name.ilike(f"%{name}%")
    )
    titles = session.exec(statement).all()
    if not titles:
        raise HTTPException(status_code=404,
                            detail=f"No projects found for year {name}.")
    return titles


# Listar os títulos de projetos lançados em determinado ano.
@router.get("/titles/{year}",
            response_model=list[str],
            status_code=status.HTTP_200_OK
            )
async def project_title_by_year(year: int,
                                session: Session = Depends(get_session)
                                ) -> list[str]:
    statement = select(Project.name).where(
        func.strftime('%Y', Project.created_at) == str(year))
    titles = session.exec(statement).all()
    if not titles:
        raise HTTPException(status_code=404,
                            detail=f"No projects found for year {year}.")
    return titles


@router.put("/{project_id}",
            response_model=Project,
            status_code=status.HTTP_200_OK
            )
async def update_project(project_id: int, update_project: Project,
                         session: Session = Depends(get_session)) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    for key, value in update_project.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    project.updated_at = datetime.now(timezone.utc)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}",
               response_model=dict,
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_project(project_id: int,
                         session: Session = Depends(get_session)) -> dict:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    session.delete(project)
    session.commit()
    return {"Message": "Project successfully deleted."}
