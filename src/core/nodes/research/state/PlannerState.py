from pydantic import BaseModel

class summary(BaseModel):
    title: str
    summary: str

class PlannerState(BaseModel):
    info_sources: list[str]
    summary_of_information: list[summary]
    intent: dict