"""Defines the cleaner agent which takes structured input and cleans the formatting while preserving the structure."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
from core.schemas.state import state

def cleaner_agent_node(prompt: str, system_prompt) -> state:
    load_dotenv()
    
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