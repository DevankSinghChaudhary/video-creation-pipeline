"""Defines the Researcher Agent which performs web research based on a given topic and prompt, utilizing specified tools for web search and date-time retrieval."""

import os
from dotenv import load_dotenv
from textwrap import dedent
import time

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware

from core.schemas.state import state, researchstate

from core.tools.web_search import web_search
from core.tools.date_time import get_date_time

from langgraph.types import Send

def fan_out_node(state: state):
    return [
        Send(
            "researcher",
            {
                "target": f"{state['topic']} - {domain}",
                "domain": domain
            }
        )
        for domain in state["domains"]
    ]

def researcher(state: state):
    load_dotenv()    

    system_prompt = dedent(
        f"""
        Research this domain.

        Return:
            - Key facts
            - Important dates
            - Statistics
            - Key stakeholders
            - Major events
            - Controversies
            - Technical explanations
            - Future implications

        Be information-dense.
        
        Topic/Domain: {state["target"]}.
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
        Analyze this topic: '{state["target"]}', create create summary about the topic.

        Domains:
        {state["domain"]}
        """
        )


    model = ChatOpenAI(model = "mistralai/mistral-nemotron",
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = os.getenv("NVIDIA_API_KEYR")
    )

    tool_limiter = ToolCallLimitMiddleware(
        tool_name='web_search',
        run_limit = 1,
        thread_limit= 3,
        exit_behavior= 'continue'

    )    

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        tools = [web_search, get_date_time],
        response_format = researchstate,
        middleware=[tool_limiter]
        )
    t = time.time()
    result  = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    print('Researcher: ', time.time() - t)
    result = result['structured_response']
    return {'research_results':[result]}
