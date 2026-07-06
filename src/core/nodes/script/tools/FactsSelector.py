import os
import time
from dotenv import load_dotenv
from textwrap import dedent
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from core.tools.web_search import web_search

class Fact(BaseModel):
    facts: list


load_dotenv()
model = ChatOpenAI(
    model = 'mistral-small-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

@tool('FactSelectorAgent', description='Use this agent to get the highest priority facts from information', return_direct=False)
def FactSelectorAgent(topic: str, intent: dict, information: list) -> dict:
    """
    Select the highest-value factual units from provided research data.

    Use this tool when the available information is too broad, redundant,
    or exceeds the short-form narration time budget.

    The tool filters research and keeps only the most important facts based on:
    - informational density
    - narrative importance
    - consequence weight
    - uniqueness
    - retention value

    Input:
    - topic: original topic
    - intent: classified topic intent
    - information: structured research units

    Output:
    - selected factual units only
    
    """


    print(f'[FactSelectorAgent] Tool Called')
    st = time.time()

    system_prompt = dedent(
        f"""
        You are FactSelectorAgent.

        Your sole responsibility is factual selection.

        You receive raw structured research.

        Your job is to identify only the highest-value facts for a short-form documentary script.

        You do NOT write.
        You do NOT summarize.
        You do NOT explain.
        You do NOT narrate.

        You only filter.

        Selection criteria:

        1. High informational density

        * facts with strong meaning per word

        2. High narrative importance

        * central events
        * major decisions
        * critical turning points

        3. High consequence weight

        * facts that caused major outcomes

        4. High uniqueness

        * avoid redundant or overlapping facts

        5. High retention value

        * surprising
        * concrete
        * measurable
        * historically important

        Prioritize:

        * dates
        * deaths
        * crashes
        * wars
        * collapses
        * discoveries
        * losses
        * measurable damage
        * scale
        * major consequences

        Avoid:

        * weak background facts
        * low-impact context
        * repetitive supporting details
        * broad explanations
        * generic filler information

        Rules:

        * Keep only what matters most.
        * Maximum 5 selected facts.
        * Minimum 3 selected facts.
        * Preserve original factual meaning exactly.
        * Do not modify facts.
        * Do not paraphrase.

        Output only valid JSON.
    """
    )

    prompt = dedent(
        f"""
        TOPIC: 
        {topic}

        INTENT:
        {intent}

        RESEARCH DATA:
        {information}

        Select the highest-value facts for short-form documentary narration.
    """
    )


    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = Fact
    )

    result = agent.invoke(
        {
            'messages': {
                'role': 'user',
                'content': prompt
                }
        }
    )
    print(f'[FactSelectorAgent] Called Finished')
    print(f'[FactSelectorAgent] {time.time()-st}')
    
    return {'ordered_facts': result['structured_response']}