from models.project import ProjectBase
from models.task import Task


class ProjecBaseWithTask(ProjectBase):
    tasks: list["Task"] = None
