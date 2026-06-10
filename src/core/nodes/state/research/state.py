from typing import TypedDict
from pydantic import BaseModel, Field
from datetime import date

class event(BaseModel):
    name: str
    date: date

class PlannerState(BaseModel):
    info_sources: list[str]
    summary_of_information: str
    any_event: bool
    if_any_event: list[event]

