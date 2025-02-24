from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

from .assignment import Assignment

if TYPE_CHECKING:
    from .task import Task


class CollaboratorBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    function: str


class Collaborator(CollaboratorBase, table=True):
    tasks: list["Task"] = Relationship(
        back_populates="collaborators",
        link_model=Assignment,
        sa_relationship_kwargs={"cascade": "save-update, merge"}
        )
