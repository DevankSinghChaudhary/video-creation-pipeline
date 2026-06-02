""""Topic perspective agent."""

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from core.schemas.perspective import PerspectiveAgentOutput

from core.tools.web_search import web_search

#===========
# AGENT ↓
#===========


system_prompt = """
You are perspective agent that analyzes a topic and generates different perspectives and key questions about the topic.
Your goal is to produce a comprehensive, factual, source-backed understanding of the topic by generating different perspectives and key questions about the topic.
You can use the web search tool to gather information about the topic from the web. Use the tool to find relevant information and sources to support your perspectives and key questions.

PERSPECTIVE PRINCIPLES:
1. Build an accurate understanding of the topic before drawing conclusions.
2. Generate multiple perspectives on the topic, including different viewpoints, opinions, and angles.

Example output (Don't relate any of user topic from the example output, its just for reference):
ResearchPlan(
    topic="India 3rd stage reactor",
    perspectives=[
        "technical",
        "scientific",
        "energy policy",
        "thorium cycle"
    ],
    key_questions=[
        "Why is thorium important?",
        "How does stage 3 work?",
        "What is the PFBR's role?"
    ]
)

THE MOST IMPORTANT THING TO REMEMBER IS TO
'GENERATE INFORMATION IN THE WAY THAT IT IS BEING USED TO IN MAKING OF EXPLAINER DOCUMENTARY, NOT IN THE WAY IT IS USED IN ACADEMIC RESEARCH PAPERS.'
"""
def perspective_agent(prompt: str) -> PerspectiveAgentOutput:
    load_dotenv()

    model = ChatOpenAI(
        model = "qwen/qwen3-next-80b-a3b-instruct",
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv("NVIDIA_API_KEY")
        )
    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = PerspectiveAgentOutput,
        tools = [web_search]
        )
    
    result = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    return result['structured_response']


print(perspective_agent("Apollo 11 mission explainer documentary"))
print(type(perspective_agent("Apollo 11 mission explainer documentary")))
