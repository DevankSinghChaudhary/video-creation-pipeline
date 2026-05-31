"""Defines the structured output schemas for the research and cleaner agents."""

from pydantic import BaseModel


#============
# Research Agent Output Structure
#============
class ResearchAgentOutput(BaseModel):
    """Structured output for the research agent."""
    topic: str
    summary: str
    number_of_queries_searched: int
    search_depth: int
    min_sources: int
    preferred_sources: list[str]    

#============
# Cleaner Agent Output Structure
#============
class CleanerAgentOutput(BaseModel):
    """Structured output for the cleaner agent."""
    topic: str
    cleaned: str
    number_of_queries_searched: int
    search_depth: int
    min_sources: int
    preferred_sources: list[str]

#============
# Researcher Config Structure
#============
class ResearcherConfig(BaseModel):
    """Configuration for the researcher agent."""
    topic: str
    search_depth: int
    min_sources: int
    preferred_sources: list[str]


#============
# Cleaner Agent Output Structure
#============
