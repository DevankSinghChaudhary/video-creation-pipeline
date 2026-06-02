"""Defines the Researcher Agent which performs web research based on a given topic and prompt, utilizing specified tools for web search and date-time retrieval."""

from datetime import datetime
from dotenv import load_dotenv
import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from schemas.research import ResearchAgentOutput

from core.tools.web_search import web_search
from core.tools.date_time import get_date_time

#================
# IMPORTS ↑
#================

load_dotenv()

#================
# MODEL ↓
#================

model = ChatOpenAI(model = "qwen/qwen3-next-80b-a3b-instruct",
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = os.getenv("NVIDIA_API_KEY")
)

#================
# AGENT ↓
#================

def researcher_agent(prompt: str, system_prompt: str) -> ResearchAgentOutput:
    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        tools = [web_search, get_date_time],
        response_format = ResearchAgentOutput
        )
    result  = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    return result['messages'][-1].content