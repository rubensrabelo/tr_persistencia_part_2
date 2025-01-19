from models.collaborator import CollaboratorBase
from models.task import Task


class CollaboratorWithTasks(CollaboratorBase):
    tasks: list["Task"] = None
