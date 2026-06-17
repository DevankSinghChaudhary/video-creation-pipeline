from pydantic import BaseModel

class asset(BaseModel):
    name: list[str]
    url: list[str]


class Scene_(BaseModel):
    title: str
    purpose: str
    narration_segment: str
    primary_visual: str
    supporting_visuals: list[str]
    assets: list[asset]

class DirectorState(BaseModel):
    visuals: list[Scene_]