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
    statement = select(func.count(Project.id))
    total = session.exec(statement).first()
    return {
        "total registered projects": total
    }


# Mostrar a quantidade de tarefas por projetos.
# Mostrar a quantidade total de projetos cadastrados por status.
# Mostrar projetos com a quantidade de tarefas estipulada.

# Task
# Mostrar a quantidade total de tarefas cadastrados por status e por projeto.
# Mostrar a quantidade de colaborador por tarefas.
# Mostrar tarefas com a quantidade de colaborador estipulada, 
# maior ou menor que...
