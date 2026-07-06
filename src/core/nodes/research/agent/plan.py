""""Planner Agent. This will give the information for the topic."""

import os
import time
from textwrap import dedent
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from core.prompt import get_systemprompt
from core.nodes.retries import with_retry
from core.nodes.research.state.PlannerState import PlannerState  
from core.nodes.state.globalstate import GlobalInformationState

from core.tools.web_search import web_search
from core.tools.date_time import get_date_time
from core.nodes.research.tools.intent import IntentAgent
from core.nodes.research.tools.context import ContextAgent
from core.nodes.research.tools.causeeffect import CauseEffectAgent

load_dotenv()

model = ChatOpenAI(
    model = 'lightning-ai/gemma-4-31B-it',
    base_url = 'https://lightning.ai/api/v1/',
    api_key = 'sk-lit-8a7f3183-3d97-4edb-9895-bb127e29a723'
)

system_prompt = get_systemprompt("planner")

@with_retry
def Researcher(state: GlobalInformationState):

    print(f'[Researcher] Started Processing')
    st = time.time()

    topic = state['topic']

    prompt = dedent(
        f"""
        [TOPIC]
        {topic}

        [ROLE]
        You are the Researcher.

        Your responsibility is to build a factual, structured research foundation for a short-form documentary typography video.

        [TASK]
        Analyze the topic and gather only the most relevant factual material needed for documentary narration.

        Your goal is to construct a structured research packet that is:

        * factual
        * high-density
        * logically connected
        * time-relevant when necessary
        * free from hallucination

        [CORE RULES]

        1. Zero hallucination.
        Use only verified information.

        2. Don't underuse web search.
        Don't over use as well, do 1-2 web search for each topic

        3. Research before synthesis.
        Do not assume facts before tool usage.

        3. Tool-first reasoning.
        Use tools whenever their output improves factual quality.

        4. Prioritize documentary-relevant information:

        * incidents
        * causes
        * consequences
        * measurable outcomes
        * timelines
        * external context

        5. Avoid collecting unnecessary background unless directly useful.

        [TOOL POLICY]

        Intent Agent:
        Use first.
        Purpose:
        Determine topic type, primary intent, and secondary intents.

        Context Agent:
        Use after Intent Agent.
        Purpose:
        Understand surrounding systems, environment, and external conditions.

        Cause And Effect Agent:
        Use when the topic involves incidents, collapses, decisions, conflicts, disasters, historical shifts, or major outcomes.
        Purpose:
        Extract causal chains and consequences.

        Web Search:
        Use after internal agents.
        Purpose:
        Collect raw factual verification, missing facts, and measurable data.

        Date and Time:
        Use when the topic is time-sensitive, historical, recent, or requires chronological grounding.

        [TOOL ORDER]

        Default order:
        Intent → Context → CauseEffect → Web Search

        Conditional:
        DateTime may be called first if time grounding is required.

        Only call tools when necessary.
        Do not call tools redundantly.
        But call websearch 1-2 times/topic

        [OUTPUT GOAL]

        Produce a structured factual research packet for downstream writing.
        Do not write the documentary itself.
        """
        )
    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = PlannerState,
        tools = [web_search, get_date_time, IntentAgent, ContextAgent, CauseEffectAgent] 
        )
    
    result = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    result = result['messages'][-1].content

    print(f'[Researcher] Finished Successfully')
    print(f'[Researcher] {time.time()-st}')

    return {'information': result}