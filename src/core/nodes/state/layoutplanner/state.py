from pydantic import BaseModel
from typing import Literal


class Asset(BaseModel):
    name: str
    role: Literal["primary", "secondary", "support"]
    scene_id: int
    importance: int
    x: float
    y: float
    z: float

class layoutstate(BaseModel):
    layout: list[Asset]