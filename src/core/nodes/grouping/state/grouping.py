from pydantic import BaseModel

class content(BaseModel):
    id: str
    text: str

class groupingschema(BaseModel):
    grouped: list[content]