"""Main entry point of the pipeline."""

from langchain.tools import tool
from langchain_openai import ChatOpenAI


from tools import web_search
from agents import researcher_agent, cleaner_agent
from core.schemas.structure import ResearchAgentOutput, CleanerAgentOutput


from dotenv import load_dotenv
import os

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

@tool("web_search", description="Search the web for information.", return_direct=False)
def search_web(query: str) -> str:
    """Search the web for information."""
    results = web_search(query)
    return results

@tool('get_current_date_time', description='Get the current date, time and year. USE IT TO RETRIEVE CURRENT DATE AND TIME.', return_direct=False)
def get_current_date_time():
    """Get the current date, time and year."""
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

#===========================
# TOOLS ↑
# ==========================

def ask_user():
    topic = input("Enter Video Topic: ")
    return topic
topic = ask_user()
prompt = f"Reseach about the topic: {topic}, create a information summary of the topic, use relevant sources from web. Make informative summary about the topic"

#===========================
# USER INPUT ↑ 
# ==========================

#----------------------------------------------------------------------------------------------------------------------------------------

#===========================
# AGENTS ↓
# ==========================

Reseacheragent = researcher_agent(
    model=model,
    prompt=prompt,
    topic=topic,
    ResearcherAgentOutput=ResearchAgentOutput,
    search_web=search_web,
    get_current_date_time=get_current_date_time
)


cleaner_prompt = f"Clean the following text: {Reseacheragent}"
Cleaneragent = cleaner_agent(
    model=model,
    prompt=cleaner_prompt,
    CleanerAgentOutput=CleanerAgentOutput
)
print(Cleaneragent['structured_response'].cleaned)
