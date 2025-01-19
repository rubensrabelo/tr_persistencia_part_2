from sqlmodel import SQLModel, Field


class Assignment(SQLModel, table=True):
    task_id: int = Field(
        default=None, foreign_key="task.id",
        primary_key=True, ondelete="CASCADE"
        )
    collaborator_id: int = Field(
        default=None, foreign_key="collaborator.id",
        primary_key=True, ondelete="CASCADE"
        )
