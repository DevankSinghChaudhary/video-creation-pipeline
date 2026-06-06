""""Topic perspective agent."""

import os
from dotenv import load_dotenv
from textwrap import dedent

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.schemas.perspective import plannerstate
from core.schemas.state import state

def planner(state: state):
    
    load_dotenv()
    topic = state['topic']


    system_prompt = dedent(
        f"""
        You are a strict, backend data-parsing agent for an educational motion graphics documentary pipeline. Your sole job is to generate a structural layout blueprint matching the requested schema exactly.

        [CRITICAL FACTUAL BOUNDARIES]
        - Rely strictly on established, verified historical and scientific facts regarding the input topic.
        - DO NOT extrapolate, hallucinate, or invent concepts, future stages, or extra chapters to inflate the list. 
        - If a national program or scientific concept has a fixed number of stages or elements, restrict your scope strictly within those boundaries.

        [VISUAL DIRECTION RULES]
        - Every domain title must represent a concrete, highly visual concept suited for vector shapes, flowcharts, code blocks, kinetic typography, or camera pans.
        - Avoid abstract, dry corporate or administrative topics (e.g., marketing, general stakeholder meetings) unless strictly necessary to the technical narrative.

        [OUTPUT FORMAT]
        - Output MUST be a clean, valid JSON/Schema structure matching the exact property definitions.
        - Absolutely NO conversational filler, introductory remarks, or concluding explanations.
        - Output ONLY the structured schema elements.
        """
        )
    prompt = dedent(
        f"""
        [Topic]
        {topic}

        [Task]
        Analyze the provided topic and break it down into a highly granular, structurally sequenced list of domains and goals for a 20-to-30 minute motion graphics documentary.

        [Execution Guidelines]
        1. Target Scope: Generate between 25 and 45 highly specific domains. Focus on technical depth, core physics, and architectural engineering over generic overviews.
        2. Sequential Flow: Order the domains logically as an episodic narrative (e.g., Scientific Hurdles -> Core Physics -> Specific Reactor Designs like AHWR/IMSBR -> Loop Mechanics -> Structural Materials -> Fuel Cycles -> Safety).
        3. Zero-Hallucination Guard: India's nuclear program has exactly 3 stages. Stage 3 is explicitly focused on Thorium utilization breeding U-233. Do not create or references stages beyond Stage 3. Align all reactor physics (thermal spectrum vs fast spectrum) precisely with real-world definitions for this stage.

        Create the domains and perspective matching the strict schema layout now.
        """
        )
    
    model = ChatOpenAI(
        model = 'lightning-ai/gpt-oss-20b',
        base_url = 'https://lightning.ai/api/v1/',
        api_key = os.getenv('OPENAI_API_KEY')
        )
    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = plannerstate,
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
    print('Planner: ', time.time() - t)
    print(result)

    return {
        'topic':topic,
        'domain': result.domain
        }