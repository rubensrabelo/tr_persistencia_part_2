from pydantic import BaseModel
from typing import Union


class ItemCount(BaseModel):
    name: str
    count: int


class GeneralResponse(BaseModel):
    description: str
    details: Union[dict[str, int], list[ItemCount]]
