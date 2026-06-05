from typing import TypedDict

# STATE CLASS
class state(TypedDict):
    topic: str
    
    domains: list[str]
    perspective: list[str]
    summary: list[str]