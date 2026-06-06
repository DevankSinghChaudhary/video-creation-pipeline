from typing import TypedDict, Annotated
from pydantic import BaseModel
import operator


# STATE CLASS
class researchstate(BaseModel):
    domain: str

    key_facts: list[str]
    timeline: list[str]
    stakeholders: list[str]
    statistics: list[str]
    controversies: list[str]

    detailed_summary: str

class state(TypedDict):
    topic: str

    domains: list[str]

    research_results: Annotated[
        list[researchstate],
        operator.add
    ]
