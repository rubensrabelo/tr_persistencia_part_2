from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_date: date = Field(default_factory=date.today)
    end_date: date | None = Field(default=None)
    completion_prediction: date
    status: str
    tasks: list["Task"] = Relationship(back_populates="project")


class Assignment(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    collaborator_id: int = Field(default=None, foreign_key="collaborator.id",
                                 primary_key=True)


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_date: date = Field(default_factory=date.today)
    end_date: date | None = Field(default=None)
    completion_prediction: date
    status: str
    project_id: int = Field(foreign_key="project.id")
    project: Project = Relationship(back_populates="tasks")
    collaborators = list["Collaborator"] = Relationship(back_populates="tasks",
                                                        link_model=Assignment)


class Collaborator(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    function: str
    tasks = list[Task] = Relationship(back_populates="collaborators",
                                      link_model=Assignment)
