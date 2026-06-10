from typing import List, TypedDict
from pydantic import BaseModel

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


class GlobalInformationState(TypedDict):
    topic: str
    information: list[PlannerState]
    script: list[ScriptState]
    visual: list[VisualState]