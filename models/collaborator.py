from sqlmodel import SQLModel, Field, Relationship
from .task import Task, Assignment  # noqa: F401


class CollaboratorBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    function: str


class Collaborator(CollaboratorBase, table=True):
    tasks = list["Task"] = Relationship(back_populates="collaborators",
                                        link_model=Assignment)
