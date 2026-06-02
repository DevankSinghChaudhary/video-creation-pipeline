from pydantic import BaseModel

class PerspectiveAgentOutput(BaseModel):
    """Schema for the output of the perspective agent."""
    topic: str
    perspectives: list[str]
    key_questions: list[str]