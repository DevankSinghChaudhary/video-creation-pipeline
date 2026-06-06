from pydantic import BaseModel

class schema(BaseModel):
    """Schema for the output of the perspective agent."""
    title: str
    goal: str

class PerspectiveAgentOutput(BaseModel):
    topic: str
    domain: list[schema]
