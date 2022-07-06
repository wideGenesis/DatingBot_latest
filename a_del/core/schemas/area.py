from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BaseArea(BaseModel):
    area: str
    city: str
    state: str
    country: str
    is_administrative_center: bool


class AreaCreate(BaseArea):
    pass


class AreaUpdate(BaseArea):
    pass


class AreaExpose(BaseArea):
    id: int

    class Config:
        orm_mode = True
