from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from starlette import status
from datetime import datetime, timezone

from database import get_session
from models.project import Project
from models.task import Task
from dto.task_dto import TaskWithCollaborator

router = APIRouter()


@router.post("/project/{project_id}",
             response_model=Task,
             status_code=status.HTTP_201_CREATED
             )
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


@router.get("/project/{project_id}",
            response_model=list[TaskWithCollaborator],
            status_code=status.HTTP_200_OK
            )
async def find_all_task_by_post_id(project_id: int,
                                   offset: int = Query(default=0, ge=0),
                                   limit: int = Query(default=10, le=100),
                                   session: Session = Depends(get_session)
                                   ) -> list[TaskWithCollaborator]:
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
@router.get("/project/{project_id}/tasks/{name}",
            response_model=list[TaskWithCollaborator],
            status_code=status.HTTP_200_OK
            )
async def find_task_by_id(project_id: int,
                          name: str,
                          session: Session = Depends(get_session)
                          ) -> list[TaskWithCollaborator]:
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


@router.put("/project/{project_id}/task/{task_id}",
            response_model=Task,
            status_code=status.HTTP_200_OK
            )
async def update_task(project_id: int,
                      task_id: int,
                      update_task: Task,
                      session: Session = Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    for key, value in update_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/project/{project_id}/task/{task_id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def delete_task(project_id: int,
                      task_id: int,
                      session: Session = Depends(get_session)
                      ):
    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    session.delete(task)
    session.commit()
