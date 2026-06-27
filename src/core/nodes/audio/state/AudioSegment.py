from pydantic import BaseModel

class AudioSegment(BaseModel):
    id: int
    path: str
    duration: float