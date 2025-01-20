from enum import Enum


class StatusEnum(str, Enum):
    NOT_DONE = "not done"
    DOING = "doing"
    DONE = "done"
