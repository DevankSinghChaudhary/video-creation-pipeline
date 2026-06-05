"""Defines the Researcher Agent which performs web research based on a given topic and prompt, utilizing specified tools for web search and date-time retrieval."""

import os
from dotenv import load_dotenv
from textwrap import dedent

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.schemas.research import ResearchAgentOutput
from core.schemas.state import state

from core.tools.web_search import web_search
from core.tools.date_time import get_date_time


def researcher_agent_node(state: state) -> ResearchAgentOutput:
    load_dotenv()    
    topic = state['topic']

    system_prompt = dedent(
        f"""
        Topic: {topic}.
        TASK: Generate summary of topic.
        FORMAT: strict schema only.
        STYLE: documentary explainer.
        INPUT: DATA THAT SHOULD BE USED TO CREATE QUERIES
        OUTPUT: no explanation.
        DOMAIN DEFINITION:
        The assigned domain is your research lens. Analyze the topic only through that domain and gather the most important facts, causes, effects, stakeholders, trends, and implications related to it.

        SEARCH STRATEGY:
            - Maximum 1-2 web_search calls.
            - Use both broad and narrow, information-dense queries.
            - Aim for maximum domain coverage per search.
        """
        )

    prompt = dedent(
        f"""
        Analyze this topic: '{topic}', create create summary about the topic.

        Domains:
        {state['domains']}
        """
        )


    model = ChatOpenAI(model = "qwen/qwen3-next-80b-a3b-instruct",
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = os.getenv("NVIDIA_API_KEYR")
    )
    
    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        tools = [web_search, get_date_time],
        response_format = ResearchAgentOutput,
        max_tool_call = 3
        )
    result  = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    return result['structured_response']