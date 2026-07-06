import os
import time
from dotenv import load_dotenv
from textwrap import dedent
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from core.tools.web_search import web_search


load_dotenv()

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

class caf(BaseModel):
    caf: list[CauseEffect]


@tool('CauseEffectAgent', description='Use this agent to get cause and effect', return_direct=False)
def CauseEffectAgent(topic, intent):
    """
    Extract the causal structure of a topic for documentary research synthesis.

    Use this tool when the topic involves events, incidents, collapses,
    decisions, conflicts, disasters, discoveries, or major outcomes where
    understanding causality improves factual depth.

    This tool identifies:

    - root causes
    - immediate triggers
    - contributing factors
    - short-term effects
    - long-term consequences
    - ripple effects

    Its purpose is to build structured causal chains.

    Think in:

    CAUSE → EVENT → EFFECT

    This tool does NOT:
    - summarize the topic
    - explain broad context
    - classify intent
    - write narration

    It focuses only on causal logic.

    Use web search when necessary for factual verification or missing causal links.

    Input:
    - topic: the raw topic string
    - intent: structured intent classification from IntentAgent
    - context: structured environmental context from ContextAgent

    Output:
    - structured cause-and-effect analysis as JSON
    """


    print(f'[CAF AGENT] Tool Called')
    st = time.time()

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
        * Don't underuse web search.
            Don't over use as well, do 1-2 web search for each topic
        * Do not explain in paragraphs.
        * Do not summarize unrelated information.
        * Focus only on causal logic.
        * Can do web search if needed (most likely, needed)

        Output only valid JSON.

        Efficiency rules:
        
        - Limit total reasoning depth.
        - Limit each output category to maximum 3 items.
        - Prefer strongest causal chain only.
        - Web search can be used 1-2 times.
        - Never expand beyond the primary causal path.
    """
    )

    prompt = dedent(
        f"""
        Topic: {topic}

        Intent: {intent}

        Analyze the causal structure of this topic.
        Extract causes and effects.
    """
    )


    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = caf,
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
    print(f'[CAF Agent] {time.time()-st}')
    print(f'[CAF Agent] Called Finished')
    
    return {'cause_effect': result['messages'][-1].content}