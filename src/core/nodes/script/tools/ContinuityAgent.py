import os
import time
from dotenv import load_dotenv
from textwrap import dedent
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool

class issue(BaseModel):
    type: str 
    between_units: list
    reason: str
        
class continuityschema(BaseModel):
    is_coherent: bool
    continuity_score: int
    issues: list[issue]

class Continuity(BaseModel):
    Continuity: list[continuityschema]


load_dotenv()
model = ChatOpenAI(
    model = 'lightning-ai/gemma-4-31B-it',
    base_url = 'https://lightning.ai/api/v1/',
    api_key = 'sk-lit-8a7f3183-3d97-4edb-9895-bb127e29a723'
)

@tool('ContinuityAgent', description='Use this agent to know the continuity of the script', return_direct=False)
def ContinuityAgent(topic: str, intent: dict, ordered_facts: dict, script: dict) -> dict:
    """
    Validate the structural continuity of an ordered factual sequence and its generated script.

    Use this tool after NarrativeFlowBuilder and script generation to inspect
    whether the factual order and written narration preserve logical integrity.

    This tool checks:

    - chronological consistency
    - causal consistency
    - missing factual bridges
    - escalation flow
    - redundancy
    - context dependency

    Its purpose is to detect structural weaknesses before final rendering.

    This tool does NOT:
    - write narration
    - rewrite narration
    - add facts
    - remove facts
    - reorder facts
    - repair continuity

    It only validates.

    Use this when:
    - the factual chain is complex
    - the topic involves multiple linked events
    - the script may contain abrupt jumps or weak transitions
    - narrative integrity needs verification

    Input:
    - topic: original user topic
    - intent: structured intent classification
    - ordered_facts: ordered factual chain from NarrativeFlowBuilder
    - script: generated documentary script

    Output:
    - continuity validation report as structured JSON
    """

    print(f'[ContinuityAgent] Tool Called')
    st = time.time()

    system_prompt = dedent(
        f"""
        You are ContinuityAgent.

        Your sole responsibility is narrative integrity validation.

        You do not write.
        You do not rewrite.
        You do not add facts.
        You do not remove facts.
        You do not reorder facts.

        You only inspect the provided ordered factual sequence and determine whether it forms a coherent documentary progression.

        Your job is to detect structural weaknesses before narration generation.

        Focus on:

        1. Chronological continuity

        * Are events ordered correctly in time?

        2. Causal continuity

        * Does each event logically connect to the next?

        3. Missing bridges

        * Is there a missing factual link required for understanding?

        4. Escalation integrity

        * Does the progression build naturally without abrupt jumps?

        5. Redundancy

        * Are any consecutive facts unnecessarily repetitive?

        6. Context dependency

        * Does a fact rely on missing prior knowledge that is absent?

        Core principle:

        Preserve factual integrity.

        Never infer beyond the provided facts.

        Never invent missing facts.

        Only flag gaps.

        Validation logic:

        Think in:

        FACT A → FACT B → FACT C

        Ask:

        * Does B logically follow A?
        * Does C logically follow B?
        * Is something required between them?
        * Is chronology broken?
        * Is causality broken?
        * Is escalation broken?

        Rules:

        * Be strict.
        * Be factual.
        * Be structural only.
        * Never narrate.
        * Never explain beyond structural logic.
        * Never repair.

        Output only valid JSON.
"""
    )

    prompt = dedent(
        f"""
        Validate the continuity of the following ordered factual units.

        Topic:
        {topic}

        Intent:
        {intent}

        Ordered Facts:
        {ordered_facts}

        Script:
        {script}

        Task:

        Inspect the sequence for structural integrity.

        Check:

        * chronological correctness
        * causal consistency
        * missing factual bridges
        * escalation flow
        * redundancy
        * context dependency

        Do not rewrite.
        Do not repair.
        Do not summarize.

        Only validate.
    """
    )


    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = Continuity
    )

    result = agent.invoke(
        {
            'messages': {
                'role': 'user',
                'content': prompt
                }
        }
    )
    print(f'[ContinuityAgent] Called Finished')
    print(f'[ContinuityAgent] {time.time()-st}')
    
    return {'continuity': result['messages'][-1].content}