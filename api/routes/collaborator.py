from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from starlette import status

from database import get_session
from models.collaborator import Collaborator
from models.collaborator_dto import CollaboratorWithTasks
from models.task import Task
from models.assignment import Assignment

router = APIRouter()


@router.post("/", response_model=Collaborator)
async def create(collaborator: Collaborator,
                 session: Session = Depends(get_session)) -> Collaborator:
    statement = select(Collaborator).where(Collaborator.email ==
                                           collaborator.email)
    collaborator_exist = session.exec(statement).first()
    if collaborator_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This email already exists.")
    session.add(collaborator)
    session.commit()
    session.refresh(collaborator)
    return collaborator


@router.post("/assignment", response_model=dict)
async def add_collaborator_in_task(assignment: Assignment,
                                   session: Session = Depends(get_session)
                                   ) -> dict:
    collaborator = session.get(Collaborator, assignment.collaborator_id)
    if not collaborator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Collaborator not found.")
    task = session.get(Task, assignment.task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found.")
    statement = (select(Assignment)
                 .where(Assignment.task_id == assignment.task_id,
                        Assignment.collaborator_id ==
                        assignment.collaborator_id))
    exist_assignment = session.exec(statement).first()
    if exist_assignment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Collaborator is already assigned.")
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return {
        "Message": "Collaborator added to task successfully.",
        "task_id": assignment.task_id,
        "collaborator_id": assignment.collaborator_id,
    }


@router.get("/", response_model=list[Collaborator])
async def find_all(offset: int = Query(default=0, ge=0),
                   limit: int = Query(default=10, le=100),
                   session: Session = Depends(get_session)
                   ) -> list[Collaborator]:
    statement = select(Collaborator).offset(offset).limit(limit)
    collaborators = session.exec(statement).all()
    return collaborators


# Find tasks title by collaborator email
@router.get("/tasks/search/email", response_model=list[CollaboratorWithTasks])
async def find_tasks_by_colaborator_email(
    email: str,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session)
) -> list[CollaboratorWithTasks]:
    statement = (select(Collaborator)
                 .where(Collaborator.email.ilike(f"%{email}%"))
                 .options(joinedload(Collaborator.tasks))
                 .offset(offset)
                 .limit(limit))
    result = session.exec(statement).unique().all()
    if not result:
        raise HTTPException(status_code=404,
                            detail="No collaborator found.")
    return result


# Listar todas as tarefas do colaborador
# Listar os nomes de colaborador nascidos em determinado ano.
@router.get("/{collaborator_id}", response_model=CollaboratorWithTasks)
async def find_by_id(collaborator_id: int,
                     session: Session = Depends(get_session)
                     ) -> CollaboratorWithTasks:
    statement = (select(Collaborator).where(Collaborator.id == collaborator_id)
                 .options(joinedload(Collaborator.tasks)))
    collaborator = session.exec(statement).first()
    if not collaborator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Collaborator not found.")
    return collaborator


@router.put("/{collaborator_id}", response_model=Collaborator)
async def update(collaborator_id: int,
                 collaborator_update: Collaborator,
                 session: Session = Depends(get_session)
                 ) -> Collaborator:
    collaborator = session.get(Collaborator, collaborator_id)
    if not collaborator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Collaborator not found.")
    for key, value in collaborator_update.model_dump(exclude_unset=True).items():
        setattr(collaborator, key, value)

    session.add(collaborator)
    session.commit()
    session.refresh(collaborator)
    return collaborator


@router.delete("/{collaborator_id}", response_model=dict)
async def delete(collaborator_id: int,
                 session: Session = Depends(get_session)
                 ) -> dict:
    collaborator = session.get(Collaborator, collaborator_id)
    if not collaborator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Collaborator not found")
    session.delete(collaborator)
    session.commit()
    return {"Message": "Collaborator successfully deleted."}
