import os
import time
from dotenv import load_dotenv
from textwrap import dedent

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.research.state import VisualState
from core.nodes.state.globalstate import GlobalInformationState
from core.prompt import get_systemprompt

load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt("illustrator")

def Illustrator(state: GlobalInformationState ):
    topic = state['topic']
    information = state['information']
    script = state['script']
    
    prompt = dedent(
        f"""
    You are an expert documentary illustrator.

    TOPIC:
    {topic}

    INFORMATION:
    {information}

    SCRIPT:
    {script}

    TASK:
    Determine what visuals should be shown to support the narration.

    GOAL:
    Generate visual concepts that maximize viewer understanding while remaining faithful to the script.

    PRIORITY:

    1. SCRIPT (highest priority)
    2. INFORMATION
    3. TOPIC

    CORE PRINCIPLE:
    Every visual must directly support, explain, reinforce, or clarify something stated or strongly implied in the script.

    VISUAL SCOPE:

    * Stay tightly aligned with the script.
    * Use the information only to better understand the script.
    * Use the topic only as additional context.
    * Do not introduce unrelated topics.
    * Do not expand into side stories.
    * Do not add facts that are not supported by the provided information.
    * Do not explore interesting but unnecessary background information.

    VISUAL THINKING:
    For each statement in the script:

    1. Identify the main subject.
    2. Identify what the viewer needs to see to understand it.
    3. Determine whether supporting context is necessary.
    4. Generate concise visual concepts.

    VISUAL TYPES MAY INCLUDE:

    * Maps
    * Historical footage
    * Archival photographs
    * People
    * Organizations
    * Locations
    * Infrastructure
    * Technology
    * Machinery
    * Events
    * Timelines
    * Comparisons
    * Rankings
    * Diagrams
    * Infographics
    * Data visualizations
    * Documents
    * Newspapers
    * Scientific illustrations
    * Satellite imagery

    ALLOWED CONTEXT EXPANSION:
    You may add supporting visuals that help explain the script.

    Example:

    Script:
    "India became the second country to operate a commercial-scale fast breeder reactor."

    Good visuals:

    * India map
    * Commercial fast breeder reactor
    * World map comparison
    * Russia highlighted as first operator
    * India highlighted as second operator

    Reason:
    These visuals help explain the statement.

    NOT ALLOWED:

    Script:
    "India became the second country to operate a commercial-scale fast breeder reactor."

    Bad visuals:

    * Complete history of India's nuclear program
    * Pokhran nuclear tests
    * China's nuclear industry
    * Global uranium trade

    Reason:
    These visuals introduce new topics not required by the script.

    QUALITY RULES:

    * Prefer specific visuals over generic visuals.
    * Prefer explanatory visuals over decorative visuals.
    * Prefer visuals that communicate information.
    * Avoid repetition.
    * Avoid redundant concepts.
    * Avoid vague descriptions.
    * Think like a documentary editor deciding what the audience should see.

    OUTPUT RULES:

    * Return only data matching the required schema.
    * Each visual should be concise.
    * Each visual should represent a single visual concept.
    * Do not provide explanations.
    * Do not provide reasoning.
    * Do not provide narration.
    * Do not provide timestamps.
    * Do not provide camera instructions.
    * Do not provide animation instructions.
    * Do not provide image prompts.
    * Do not provide video prompts.
    * Do not provide markdown.

    OUTPUT:
    Return only the visual concepts.
    """
    )

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = VisualState
    )

    t = time.time()
    result = agent.invoke({
        'messages':{
            'role':'user',
            'content': prompt
        }
    })
    print("Illustrator: ", time.time() - t)

    result = result['structured_response']
    return {
        'visual': result
    }