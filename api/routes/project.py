from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from starlette import status
from datetime import datetime, timezone

from database import get_session
from models.project import Project, ProjecBaseWithTask
from models.task import Task, TaskWithProjectAndCollaborator

router = APIRouter()


# Project
@router.post("/", response_model=Project)
async def create_project(project: Project,
                         session: Session = Depends(get_session)) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


# Listar todos os projetos
@router.get("/", response_model=list[ProjecBaseWithTask])
async def find_all_project(offset: int = Query(default=0, ge=0),
                           limit: int = Query(default=10, le=100),
                           session: Session = Depends(get_session)
                           ) -> list[ProjecBaseWithTask]:
    statement = (select(Project).offset(offset).limit(limit)
                 .options(joinedload(Project.tasks)))
    projects = session.exec(statement).unique().all()
    return projects


# Mostrar um projeto por id
@router.get("/{project_id}", response_model=ProjecBaseWithTask)
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


# Listar os títulos de projetos lançados em determinado ano.
@router.get("/titles/{year}", response_model=list[str])
async def project_title_by_year(year: int,
                                session: Session = Depends(get_session)
                                ) -> list[str]:
    statement = select(Project.name).where(
        func.strftime('%Y', Project.created_at) == str(year))
    titles = session.exec(statement).all()
    print(titles)
    if not titles:
        raise HTTPException(status_code=404,
                            detail=f"No projects found for year {year}.")
    return titles


# Listar os títulos de projetos cujo título contém determinada string.
@router.get("/title-name/search", response_model=list[str])
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


@router.put("/{project_id}", response_model=Project)
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


@router.delete("/{project_id}", response_model=dict)
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
@router.post("/{project_id}/tasks/",
             response_model=Task)
async def create_task_for_project(project_id: int,
                                  task: Task,
                                  session: Session = Depends(get_session)
                                  ) -> Task:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    task.project_id = project_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{project_id}/tasks/",
            response_model=list[TaskWithProjectAndCollaborator])
async def find_all_task_by_post_id(project_id: int,
                                   offset: int = Query(default=0, ge=0),
                                   limit: int = Query(default=10, le=100),
                                   session: Session = Depends(get_session)
                                   ) -> list[TaskWithProjectAndCollaborator]:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    statement = (select(Task)
                 .where(Task.project_id == project_id)
                 .offset(offset)
                 .limit(limit)
                 .options(joinedload(Task.collaborators)))
    tasks_by_project = session.exec(statement).unique().all()
    return tasks_by_project


# Listar tasks por nome
@router.get("/{project_id}/tasks/{name}",
            response_model=list[TaskWithProjectAndCollaborator])
async def find_task_by_id(project_id: int,
                          name: str,
                          session: Session = Depends(get_session)
                          ) -> list[TaskWithProjectAndCollaborator]:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    statement = (select(Task).where(Task.project_id == project_id,
                                    Task.name.ilike(f"%{name}%"))
                 .options(joinedload(Task.project),
                          joinedload(Task.collaborators)))
    task = session.exec(statement).unique().all()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found.")
    return task


@router.put("/{project_id}/tasks/{task_id}", response_model=Task)
async def update_task(project_id: int,
                      task_id: int,
                      task: Task,
                      session: Session = Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{project_id}/tasks/{task_id}", response_model=dict)
async def delete_task(project_id: int,
                      task_id: int,
                      session: Session = Depends(get_session)) -> dict:
    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    session.delete(task)
    session.commit()
    return {"Message": "Task successfully deleted."}
