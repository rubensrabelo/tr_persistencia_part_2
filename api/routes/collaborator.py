from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from starlette import status

from database import get_session
from models.collaborator import Collaborator
from models.task import Task, Assignment

router = APIRouter()


@router.post("/", response_model=Collaborator)
async def create(collaborator: Collaborator,
                 session: Session = Depends(get_session)) -> Collaborator:
    session.add(collaborator)
    session.commit()
    session.refresh(collaborator)
    return collaborator


@router.post("/{collaborator_id}/task/{task_id}", response_model=dict)
async def add_collaborator_in_task(collaborator_id: int,
                                   task_id: int,
                                   session: Session = Depends(get_session)
                                   ) -> dict:
    collaborator = session.get(Collaborator, collaborator_id)
    if not collaborator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Collaborator not found.")
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found.")
    assignment = Assignment(task_id=task_id, collaborator_id=collaborator_id)
    session.add(assignment)
    session.commit()
    return {"Message": "Collaborator added successfully"}


@router.get("/", response_model=Collaborator)
async def find_all(skip: int = 0, limit: int = 10,
                   session: Session = Depends(get_session)
                   ) -> list[Collaborator]:
    statement = select(Collaborator).offset(skip).limit(limit)
    collaborators = session.exec(statement).all
    return collaborators


@router.get("/{collaborator_id}", response_model=Collaborator)
async def find_by_id(collaborator_id: int,
                     session: Session = Depends(get_session)) -> Collaborator:
    collaborator = session.get(Collaborator, collaborator_id)
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
    for key, value in collaborator_update.model_dump().items:
        setattr(collaborator, key, value)

    session.add(collaborator)
    session.commit()
    session.refresh(collaborator)
    return collaborator


@router.delete("/{collaborator_id}", response_model=Collaborator)
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
