from pydantic import BaseModel

class ScriptState(BaseModel):
    script: list[str]