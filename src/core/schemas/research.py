"""Defines the structured output schemas for the research and cleaner agents."""

from pydantic import BaseModel


#============
# Research Agent Output Structure
#============
class ResearchState(BaseModel):
    domain: str
    domain_info_summary: str