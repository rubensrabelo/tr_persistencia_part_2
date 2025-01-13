from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from .project import Project
from .collaborator import Collaborator


class Assignment(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    collaborator_id: int = Field(default=None, foreign_key="collaborator.id",
                                 primary_key=True)


class TaskBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_date: date = Field(default_factory=date.today)
    end_date: date | None = Field(default=None)
    completion_prediction: date
    status: str


class Task(TaskBase, table=True):
    project_id: int = Field(foreign_key="project.id")
    project: "Project" = Relationship(back_populates="tasks")
    collaborators = list["Collaborator"] = Relationship(back_populates="tasks",
                                                        link_model=Assignment)


class TaskWithProjectAndCollaborator(TaskBase):
    project: "Project" | None
    collaborators: list["Collaborator"] = None
