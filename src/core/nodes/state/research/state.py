from typing import TypedDict
from pydantic import BaseModel
from core.nodes.state.director.state import DirectorState

class summary(BaseModel):
    title: str
    summary: str

class PlannerState(BaseModel):
    info_sources: list[str]
    summary_of_information: list[summary]

class script_breakdown(BaseModel):
    id: int
    script: str

class ScriptState(BaseModel):
    script_: list[script_breakdown]


class VisualState(BaseModel):
    visual: list[str] 