from pydantic import BaseModel

#============
# Cleaner Agent Output Structure
#============
class CleanerAgentOutput(BaseModel):
    topic: str
    cleaned: str
    number_of_queries_searched: int
    search_depth: int
    sources: int
    preferred_sources: list[str]