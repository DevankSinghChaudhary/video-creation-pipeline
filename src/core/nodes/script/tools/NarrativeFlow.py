import os
import time
from dotenv import load_dotenv
from textwrap import dedent
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool

class flowschema(BaseModel):
    flow_type: str
    ordered_facts: list

class Flow(BaseModel):
    Flow: list[flowschema]


load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

@tool('NarrativeFlowBuilder', description='Use this agent to get the Narrative Flow of the facts', return_direct=False)
def NarrativeFlowBuilder(topic: str, intent: dict, selected_facts: list) -> dict:
    """
    Arrange selected factual units into the strongest documentary narrative flow.

    Use this tool after fact selection when facts exist but their order
    is weak, unclear, or not optimized for retention.

    The tool reorders facts into logical documentary structures such as:
    - trigger → cause → escalation → consequence
    - timeline progression
    - collapse progression
    - conflict progression

    It does not write narration.
    It only structures factual order.

    Input:
    - topic: original topic
    - intent: classified topic intent
    - selected_facts: filtered factual units

    Output:
    - ordered factual units in strongest narrative progression
    """

    print(f'[NarrativeFlowBuilder] Tool Called')
    st = time.time()

    system_prompt = dedent(
        f"""
        You are NarrativeFlowBuilder.

        Your only responsibility is narrative ordering.

        You receive already-selected factual units.

        Your job is to arrange them into the strongest documentary flow.

        You do NOT write narration.
        You do NOT summarize.
        You do NOT explain.
        You do NOT invent.
        You do NOT remove facts.

        You only reorder.

        Goal:

        Transform raw selected facts into a high-retention documentary progression.

        Preferred structural patterns:

        1. Incident Flow
        Trigger → Cause → Escalation → Consequence → Impact

        2. Timeline Flow
        Earliest → Progression → Turning Point → Outcome

        3. Collapse Flow
        Peak → Weakness → Trigger → Collapse → Aftermath

        4. Discovery Flow
        Problem → Discovery → Mechanism → Result → Impact

        5. Conflict Flow
        Tension → Cause → Action → Result → Consequence

        Rules:

        * Preserve factual meaning exactly.
        * Keep all selected facts.
        * No paraphrasing.
        * No expansion.
        * No interpretation.
        * Order for maximum logical clarity and retention.

        Priority rules:

        * strongest hook-worthy fact first
        * causal clarity second
        * consequence weight last

        Output only valid JSON.
    """
    )

    prompt = dedent(
        f"""
        TOPIC: {topic}

        INTENT: {intent}

        SELECTED FACTS:
        {selected_facts}

        Reorder these facts into the strongest documentary narrative flow.
        """
    )


    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = Flow
    )

    result = agent.invoke(
        {
            'messages': {
                'role': 'user',
                'content': prompt
                }
        }
    )
    print(f'[NarrativeFlowBuilder] Called Finished')
    print(f'[NarrativeFlowBuilder] {time.time()-st}')
    
    return {'flow': result['structured_response']}