"""Main entry point of the pipeline."""

from textwrap import dedent
from datetime import datetime
from dotenv import load_dotenv
import json
import os

from langchain.tools import tool
from langchain_openai import ChatOpenAI

from agents.perspective import perspective_agent
from agents.cleaner import cleaner_agent
from agents.researcher import researcher_agent

from schemas.research import ResearchAgentOutput
from core.schemas.perspective import PerspectiveAgentOutput
from schemas.cleaner import CleanerAgentOutput



#===========================
# IMPORTS ↑
# ==========================

load_dotenv()

model = ChatOpenAI(model = "qwen/qwen3-next-80b-a3b-instruct",
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = os.getenv("NVIDIA_API_KEY")
)

#===========================
# MODEL ↑
# ==========================

def ask():
    while True:
        topic = input("Enter Video Topic: ")
        if topic.strip() != "":
            return topic
        print("Topic cannot be empty. Please enter a valid topic.")

topic = ask()

#===========================
# USER INPUT ↑ 
# ==========================

#----------------------------------------------------------------------------------------------------------------------------------------

#===========================
# PROMPTS ↓
# ==========================

system_prompt = dedent(f"""
You are a professional documentary research agent.

Your goal is to produce a comprehensive, factual, source-backed understanding of:

TOPIC:
{topic}

RESEARCH PRINCIPLES:

1. Build an accurate understanding of the topic before drawing conclusions.

2. Generate multiple search queries covering:
   - Background
   - Timeline
   - Key people
   - Major events
   - Technical details (if applicable)
   - Consequences and significance
   - Statistics and evidence

3. Use available tools to gather information from diverse, high-quality sources.

4. Continuously identify gaps in knowledge and perform additional targeted searches to fill those gaps.

5. Prioritize:
   - Government sources
   - Academic sources
   - Official documentation
   - Books and archives
   - Reputable news organizations
   - Subject matter experts

6. Cross-check important claims whenever possible.

7. Remove:
   - Navigation text
   - Social media links
   - Advertisements
   - Related articles
   - Recommended content
   - Search engine artifacts
   - Website boilerplate

8. Focus on extracting facts, evidence, explanations, timelines, and important context.

9. Preserve important details while eliminating redundancy.

10. Produce a clear, structured, informative summary suitable for documentary production.

Your output must include:
- topic
- summary
- search_depth
- number_of_queries_searched
- sources
- preferred_sources
""")

prompt = dedent(f"""
Analyze about topic: {topic} and create a summary, all other instructions are in system prompt.""")
