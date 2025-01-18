from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from starlette import status
from datetime import datetime, timezone

from database import get_session
from models.project import Project
from models.task import Task
from models.collaborator import Collaborator
from models.assignment import Assignment

router = APIRouter()


# Project
# Mostrar a quantidade total de projetos cadastrados.
@router.get("/projects/total", response_model=dict)
async def total_registered_projects(session: Session = Depends(get_session)
                                    ) -> dict:
    statement = (select(func.count(Project.id)))
    total = session.exec(statement).first()
    return {
        "total registered projects": total
    }


# Mostrar a quantidade de tarefas por projetos.
# Mostrar projetos com a quantidade de tarefas estipulada.
@router.get("/projects/total/tasks", response_model=dict[str, int])
async def total_task_by_project(session: Session = Depends(get_session)
                                ) -> dict[str, int]:
    statement = (select(Project.name, func.count(Task.id).label("task_count"))
                 .join(Task, isouter=True)
                 .group_by(Project.id))
    result = session.exec(statement).all()
    result_dict = {project_name: task_count
                   for project_name, task_count in result}
    return result_dict


# Mostrar a quantidade total de projetos cadastrados por status.
@router.get("/projects/total/status", response_model=dict)
async def total_projects_by_status(status_project: str = None,
                                   session: Session = Depends(get_session)
                                   ) -> dict:
    if status_project:
        statement = (
            select(func.count(Project.id))
            .where(Project.status == status_project))
        result = session.exec(statement).first()
        return {
            f"Total {status_project}": result
        }
    else:
        statement = (
            select(Project.status, func.count(Project.id).label("status_count"))
            .group_by(Project.status))
        result = session.exec(statement).all()
        return {
            row.status: row.status_count
            for row in result
        }


# Task
# Mostrar a quantidade total de tarefas cadastrados por status e por projeto.
# Mostrar a quantidade de colaborador por tarefas.
# Mostrar tarefas com a quantidade de colaborador estipulada,
# maior ou menor que...
