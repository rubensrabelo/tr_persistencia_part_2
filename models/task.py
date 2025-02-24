from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from .collaborator import Collaborator
from .assignment import Assignment
from .enum.status_enum import StatusEnum

if TYPE_CHECKING:
    from .project import Project


class TaskBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    status: StatusEnum = Field(default=StatusEnum.NOT_DONE)


class Task(TaskBase, table=True):
    project_id: int = Field(foreign_key="project.id", ondelete="CASCADE")
    project: "Project" = Relationship(
        back_populates="tasks"
        )
    collaborators: list["Collaborator"] = Relationship(
        back_populates="tasks",
        link_model=Assignment,
        sa_relationship_kwargs={"cascade": "save-update, merge"}
        )
