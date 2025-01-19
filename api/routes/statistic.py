from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from sqlalchemy.sql import func
from starlette import status

from database import get_session
from models.project import Project
from models.task import Task
from models.assignment import Assignment
from dto.statistic_dto import ItemCount, GeneralResponse

router = APIRouter()


# Project
# Mostrar a quantidade total de projetos cadastrados.
@router.get("/projects/total", response_model=ItemCount)
async def total_registered_projects(session: Session = Depends(get_session)
                                    ) -> ItemCount:
    statement = (select(func.count(Project.id)))
    total = session.exec(statement).first()
    return ItemCount(
        name="Total number of registered projects.",
        count=total
    )


# Mostrar a quantidade de tarefas por projetos.
# Mostrar projetos com a quantidade de tarefas estipulada.
@router.get("/projects/total/tasks/filtered", response_model=GeneralResponse)
async def total_task_by_project(min_tasks: int = 0,
                                max_tasks: int | None = None,
                                session: Session = Depends(get_session)
                                ) -> GeneralResponse:
    count_tasks = func.count(Task.id).label("task_count")
    statement = (select(Project.name, count_tasks)
                 .join(Task, isouter=True)
                 .group_by(Project.id)
                 .having(count_tasks >= min_tasks))
    if max_tasks:
        statement = statement.having(count_tasks <= max_tasks)
    result = session.exec(statement).all()
    items = [
        ItemCount(name=project_name, count=task_count) for project_name,
        task_count in result
        ]
    return GeneralResponse(
        description="Number of tasks per project.",
        details=items
    )


# Mostrar a quantidade total de projetos cadastrados por status.
@router.get("/projects/total/status", response_model=GeneralResponse)
async def total_projects_by_status(status_project: str = None,
                                   session: Session = Depends(get_session)
                                   ) -> GeneralResponse:
    if status_project:
        statement = (
            select(func.count(Project.id))
            .where(Project.status == status_project)
            )
        result = session.exec(statement).first()
        return GeneralResponse(
            description=f"Total projects with status '{status_project}'.",
            details={f"Total {status_project}": result}
        )
    else:
        statement = (
            select(Project.status, func.count(Project.id).label(
                "status_count"))
            .group_by(Project.status))
        result = session.exec(statement).all()
        details = [
            ItemCount(name=row.status, count=row.status_count)
            for row in result
            ]
        return GeneralResponse(
            description="Total projects grouped by status.",
            details=details
        )


# Task
# Mostrar a quantidade total de tarefas cadastrados por status e por projeto.
@router.get("/projects/{project_id}/tasks/total/status",
            response_model=GeneralResponse)
async def total_tasks_by_status_and_project_id(project_id: int,
                                               session: Session = Depends(
                                                   get_session)
                                               ) -> GeneralResponse:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found.")
    statement = (
        select(Task.status, func.count(Task.id).label("task_count"))
        .where(Task.project_id == project_id)
        .group_by(Task.status)
    )
    result = session.exec(statement).all()
    details = [
        ItemCount(name=status_proj, count=task_count)
        for status_proj, task_count in result
        ]
    return GeneralResponse(
        description="Total tasks by status for project.",
        details=details
    )


# Mostrar a quantidade de colaborador por tarefas.
# Mostrar tarefas com a quantidade de colaborador estipulada
@router.get("/tasks/total/collaborators/filtered/projects/{project_id}",
            response_model=GeneralResponse)
async def total_collaborators_by_task_and_project(
    project_id: int,
    min_collaborators: int = 0,
    max_collaborators: int = None,
    session: Session = Depends(get_session)
) -> GeneralResponse:
    count_collaborators = func.count(Assignment.collaborator_id).label(
        "collaborator_count")
    statement = (
        select(Task.name, count_collaborators)
        .join(Task, Assignment.task_id == Task.id)
        .join(Project, Project.id == Task.project_id)
        .filter(Project.id == project_id)
        .group_by(Task.id)
        .having(count_collaborators >= min_collaborators)
    )

    if max_collaborators:
        statement = statement.having(count_collaborators <= max_collaborators)
    result = session.exec(statement).all()
    details = [
        ItemCount(name=task_name, count=collaborator_count)
        for task_name, collaborator_count in result
        ]
    return GeneralResponse(
        description="Number of collaborators per project tasks.",
        details=details
    )
