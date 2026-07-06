import os
import time
import json
from dotenv import load_dotenv
from textwrap import dedent
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from core.tools.web_search import web_search

system_prompt = dedent(
        f"""
        You are CauseEffectAgent.

        Your role is to identify causal relationships surrounding a topic.

        You analyze events, systems, decisions, or phenomena and determine:

        * what caused it
        * what influenced it
        * what accelerated it
        * what resulted from it
        * what changed because of it

        Your goal is to extract causal chains.

        Think in:

        CAUSE → EVENT → EFFECT

        Focus on:

        1. Root causes
        2. Immediate triggers
        3. Contributing factors
        4. Short-term effects
        5. Long-term consequences
        6. Ripple effects

        Rules:

        * Be factual.
        * Do not narrate.
        * Do not explain in paragraphs.
        * Do not summarize unrelated information.
        * Focus only on causal logic.
        * Do web searches

        OUTPUT:
        ONLY JSON, NO INITAL TEXT
        """
    )

d = {
    "primary_intent": "History",
    "secondary_intents": ["News"],
    "content_structure": "Documentary",
    "tone": "Neutral",
    "complexity": "Low"
    }
prompt = dedent(
        f"""
        Topic: {'India Reached 3rd Stage Reactor'}

        Intent: {d}

        Analyze the causal structure of this topic.
        Extract causes and effects.
    """
    )


mistral='xxi2rLrwl4LdFfnluFRj97O96ShkHds3'



load_dotenv()

model1 = ChatOpenAI(
    model = 'mistral-small-2506',
    base_url = 'https://api.mistral.ai/v1',
    api_key = mistral
)
model2 = ChatOpenAI(
    model = 'ministral-8b-2512',
    base_url = 'https://api.mistral.ai/v1',
    api_key = mistral
)
model = ChatOpenAI(
    model = 'ministral-14b-2512',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)


class CauseEffect(BaseModel):
    root_causes: list[str]
    immediate_triggers: list[str]
    contributing_factors: list[str]
    short_term_effects: list[str]
    long_term_effects: list[str]
    ripple_effects: list[str]

class Effect(BaseModel):
    output: list[CauseEffect]

def CauseEffectAgent():

    print(f'[CAF AGENT] Tool Called')
    st = time.time()

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        tools = [web_search],
        response_format = Effect
    )

    result = agent.invoke({'messages':{'role':'user','content':prompt}})

    result = result['messages'][-1].content
    print(f'[CAF Agent] {time.time()-st}')
    print(f'[CAF Agent] Called Finished')
    print()
    return result

    

d = {
    "primary_intent": "History",
    "secondary_intents": ["News"],
    "content_structure": "Documentary",
    "tone": "Neutral",
    "complexity": "Low"
    }
print(CauseEffectAgent())