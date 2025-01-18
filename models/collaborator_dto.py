from .collaborator import CollaboratorBase
from .task import Task


class CollaboratorWithTasks(CollaboratorBase):
    tasks: list["Task"] = None
