import os
import time
from dotenv import load_dotenv
from textwrap import dedent
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from core.tools.web_search import web_search

class contextschema(BaseModel):
    Environment: list
    external_factors: list
    competing_forces: list
    systemic_conditions: list
    relevant_background: list

class Context(BaseModel):
    context: list[contextschema]


load_dotenv()
model = ChatOpenAI(
    model = 'mistral-small-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

@tool('ContextAgent', description='Use this agent to get topic overall context', return_direct=False)
def ContextAgent(topic, intent):
    """
    Extract the surrounding context of a topic for deeper research synthesis.

    Use this tool after IntentAgent when the topic requires environmental,
    systemic, or external understanding beyond the core subject itself.

    This tool identifies the broader conditions that shaped the topic, including:
    - environmental conditions
    - external pressures
    - competing forces
    - systemic influences
    - relevant historical background

    Its purpose is to answer:

    "What was happening around this topic that made it possible, important, or inevitable?"

    This tool does NOT:
    - summarize the topic directly
    - extract causes
    - write narration
    - classify intent

    It focuses only on surrounding context.

    Use web search when necessary for factual grounding.

    Input:
    - topic: the raw topic string
    - intent: structured intent classification from IntentAgent

    Output:
    - structured contextual analysis as JSON
    """


    print(f'[ContextAgent] Tool Called')
    st = time.time()

    system_prompt = dedent(
        f"""
        You are ContextAgent.

        Your role is to identify the surrounding environment, systems, and conditions that shaped the given topic.

        You do not focus on the topic directly.

        You focus on:

        * external factors
        * industry conditions
        * political climate
        * technological landscape
        * economic pressures
        * cultural influences
        * competing systems
        * historical circumstances

        Your purpose is to answer:

        "What was happening around this topic that made it possible, important, or inevitable?"

        Rules:

        * Do not summarize the topic itself.
        * Focus only on surrounding context.
        * Be factual and concise.
        * Extract only relevant context.
        * Ignore unrelated background.
        * Don't underuse web search.
            Don't over use as well, do 1-2 web search for each topic

        Output only structured JSON.
    """
    )

    prompt = dedent(
        f"""
        Topic: {topic}
        Primary intent: {intent}
        """
    )


    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = Context,
        tools = [web_search]
    )

    result = agent.invoke(
        {
            'messages': {
                'role': 'user',
                'content': prompt
                }
        }
    )
    print(f'[ContextAgent] Called Finished')
    print(f'[ContextAgent] {time.time()-st}')
    
    return {'context': result['structured_response']}