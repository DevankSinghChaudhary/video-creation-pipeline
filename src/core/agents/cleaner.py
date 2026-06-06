"""Defines the cleaner agent which takes structured input and cleans the formatting while preserving the structure."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
from textwrap import dedent

from core.schemas.state import state



def cleaner_agent_node(state: state) -> state:
    load_dotenv()
    
    system_prompt = dedent(
        f"""
        TASK: Remove all formatting, if any.
        Fomatting_example: '\\n', 'n', '\\', '\\\\' etc 
        """
        )

    prompt = dedent(
        f"""
        DATA: {state['summary']}
        """
        )

    model = ChatOpenAI(
        model = "nvidia/nemotron-3-ultra-550b-a55b",
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv("NVIDIA_API_KEYC"),
        )
    agent =create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = state
        )
    
    result = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    
    return result['structured_response']