from pydantic import BaseModel

class PerspectiveAgentOutput(BaseModel):
    """Schema for the output of the perspective agent."""
    domains: list[str]
    perspectives: list[str]