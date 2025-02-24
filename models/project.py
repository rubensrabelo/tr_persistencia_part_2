from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

from .task import Task
from .enum.status_enum import StatusEnum


class ProjectBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    status: StatusEnum = Field(default=StatusEnum.NOT_DONE)


class Project(ProjectBase, table=True):
    tasks: list["Task"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
        )
