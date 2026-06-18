""""Topic perspective agent."""

import os
from textwrap import dedent
from dotenv import load_dotenv
from qdrant_client import QdrantClient

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from core.prompt import get_systemprompt 
from core.tools.web_search import web_search
from core.tools.date_time import get_date_time
from core.nodes.state.research.state import PlannerState  
from core.nodes.state.globalstate import GlobalInformationState



load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)
system_prompt = get_systemprompt("planner")

def Planner(state: GlobalInformationState):

    topic = state['topic']

    prompt = dedent(
        f"""
        [Topic]
        {topic}

        [Task]
        Analyze the provided topic and break it down into a highly granular, structurally sequenced list of domains and goals for a 20-to-30 minute motion graphics documentary.

        [Execution Guidelines]
        1. Target Scope: Generate between 5-10 strict highly specific domains. Focus on technical depth, core physics, and architectural engineering over generic overviews.
        2. Sequential Flow.
        3. Zero-Hallucination about the topic.
        """
        )
    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = PlannerState,
        tools = [web_search, get_date_time] 
        )
    import time
    t = time.time()
    result = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    result = result['messages'][-1].content
    print('Planner: ', time.time() - t)
    return {
        'information': result
        }