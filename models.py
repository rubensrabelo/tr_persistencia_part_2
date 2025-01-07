from datetime import date
from sqlmodel import SQLModel, Field


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_date: date = Field(default_factory=date.today)
    end_date: date | None = Field(default=None)
    completion_prediction: date
    status: str


# class Assignment(SQLModel, table=True):
#     task_id: "Task"
#     collaborator_id: "Collaborator"
#     assignment_date: date


# class Task(SQLModel, table=True):
#     id: int | None
#     name: str
#     description: str
#     start_date: date
#     end_date: date | None
#     completion_prediction: date
#     status: str
#     project_id: Project


class Collaborator(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    function: str
