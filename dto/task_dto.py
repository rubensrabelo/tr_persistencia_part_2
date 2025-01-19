from models.project import Project
from models.collaborator import Collaborator
from models.task import TaskBase


class TaskWithCollaborator(TaskBase):
    collaborators: list["Collaborator"] = None

