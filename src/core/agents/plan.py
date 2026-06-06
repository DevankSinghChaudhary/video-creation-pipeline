""""Topic perspective agent."""

import os
from dotenv import load_dotenv
from textwrap import dedent

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.schemas.perspective import PerspectiveAgentOutput
from core.schemas.state import state

def planner(state: state):
    
    load_dotenv()
    topic = state['topic']


    system_prompt = dedent(
        f"""
        Topic: {topic}.
        TASK: Generate ResearchPlan for documentary.
        FORMAT: strict schema only.
        STYLE: documentary explainer.
        DOMAIN: auto-infer.
        OUTPUT: no explanation.
        """
        )
    prompt = dedent(
        f"""
        Analyze this topic: '{topic}', create domains and perspective.
        """
        )
    
    model = ChatOpenAI(
        model = 'mistralai/mistral-nemotron',
        base_url = 'https://integrate.api.nvidia.com/v1',
        api_key = os.getenv('NVIDIA_API_KEYP')
        )
    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = PerspectiveAgentOutput,
        )
    import time
    t = time.time()
    result = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    result = result['structured_response']
    print('Perspective: ', time.time() - t)
    return {
        'domains': result.domains, 
        'perspectives': result.perspectives
        }