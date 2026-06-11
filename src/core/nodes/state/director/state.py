from pydantic import BaseModel


class Scene_(BaseModel):
    title: str
    purpose: str
    narration_segment: str
    primary_visual: str
    supporting_visuals: list[str]

class DirectorState(BaseModel):
    visuals: list[Scene_]