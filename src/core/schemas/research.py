"""Defines the structured output schemas for the research and cleaner agents."""

from pydantic import BaseModel


#============
# Research Agent Output Structure
#============
class ResearchAgentOutput(BaseModel):
    """Structured output for the research agent.
    Depth refers to how many layers of information the agent has searched through. For example, if the agent searches for a topic, then searches for related subtopics, and then searches for information on those subtopics, that would be a depth of 3.
    Sources refers to the number of different sources the agent has consulted to gather information on the topic. This could include websites, articles, books, or any other type of source that provides relevant information.
    Preferred sources refers to the specific sources that the agent has identified as being particularly useful or relevant for the topic at hand. These could be sources that are known to be reliable, comprehensive, or particularly insightful on the topic.
    HAVE TO INCREASE DEPTH ON EACH OUTPUT.
    """
    topic: str
    summary: str
    number_of_queries_searched: int
    search_depth: int
    sources: int
    preferred_sources: list[str]    
