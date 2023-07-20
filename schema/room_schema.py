from pydantic import BaseModel as PydanticBaseModel, Field, validator
from typing import Union


class BaseModel(PydanticBaseModel):
    class config:
        orm_mode = True

class RoomBase(BaseModel):
    center_id: int = Field(gt=0)
    name: str = Field(min_lenght=4)
    description: str = Union [str, None]