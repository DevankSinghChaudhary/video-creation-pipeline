from pydantic import BaseModel

class script_breakdown(BaseModel):
    id: int
    script: str

class FormatterState(BaseModel):
    script_: list[script_breakdown]