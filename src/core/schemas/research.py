"""Defines the structured output schemas for the research and cleaner agents."""

from pydantic import BaseModel


#============
# Research Agent Output Structure
#============
class Researchstate(BaseModel):
    domain: str
    domain_info_summary: str