import os
import time
from textwrap import dedent
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

class intentschema(BaseModel):
    primary_intent: str
    secondary_intents: list[str]
    content_structure: str
    tone: str
    complexity: str

class IntentState(BaseModel):
    intent: list[intentschema]


load_dotenv()

model = ChatOpenAI(
    model = 'mistral-small-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

@tool('intent', description='This tool is for knowing intent behind the topic user entered', return_direct=False)
def IntentAgent(topic):
    """
    Extract the structural intent of a given topic for downstream research planning.

    Use this tool at the beginning of the research phase to classify:
    - the primary subject domain
    - secondary supporting domains
    - content structure
    - emotional tone
    - conceptual complexity

    This tool performs classification only.

    It does NOT:
    - explain the topic
    - write scripts
    - research facts
    - generate narration

    Its output is used by downstream agents to decide:
    - what research path to take
    - what specialized tools to call
    - what narrative structure to build
    - what writing style to follow

    Input:
    - topic: the raw topic string provided by the user

    Output:
    - structured intent classification as JSON
    """


    print(f"[Intent] Tool Called")
    st = time.time()

    system_prompt = dedent(
        f"""You are IntentAgent.

        Your sole responsibility is intent extraction.

        You analyze a topic and determine its informational intent, structural nature, and content requirements for downstream planning agents.

        You do not write scripts.
        You do not explain topics.
        You do not add facts.
        You do not speculate.

        Your output is used by other agents to decide:

        * what research path to take
        * what narrative structure to use
        * what specialized sub-agents to call
        * what visual strategy to apply

        Your job is classification only.

        Classify the topic across these dimensions:

        1. Primary intent:
        Identify the dominant subject domain.

        Possible domains:
        HISTORY
        SCIENCE
        DOCUMENTARY
        BIOGRAPHY
        GEOPOLITICS
        ECONOMICS
        PSYCHOLOGY
        PHILOSOPHY
        TECHNOLOGY
        SPORTS
        CRIME
        MILITARY
        CULTURE
        MYSTERY

        2. Secondary intents:
        Identify supporting domains if applicable.

        3. Content structure:
        Determine the best structural form.

        Possible values:
        EXPLANATORY
        NARRATIVE
        TIMELINE
        ANALYTICAL
        COMPARATIVE
        BREAKDOWN
        CASE_STUDY

        4. Tone:
        Determine the natural emotional tone.

        Possible values:
        SERIOUS
        NEUTRAL
        DARK
        INSPIRING
        TENSE
        CURIOUS

        5. Complexity:
        Estimate conceptual depth.

        Possible values:
        LOW
        MEDIUM
        HIGH

        Rules:

        * Output only valid JSON.
        * Never output prose.
        * Never explain reasoning.
        * Never generate content beyond classification.
        * If uncertain, choose the most probable interpretation.
    """
    )

    prompt = dedent(
        f"""
        You are IntentAgent.

        Your task is to analyze the given topic and identify the core content intent behind it.

        Determine what kind of informational video this topic should become.

        Focus only on intent classification, not writing, explanation, or storytelling.

        Classify the topic into one or more of these categories:

        * HISTORY → past events, timelines, wars, civilizations, biographies, origins
        * SCIENCE → physics, biology, chemistry, astronomy, technology explanations
        * DOCUMENTARY → real-world systems, organizations, infrastructure, hidden operations
        * BIOGRAPHY → life of a person, rise/fall, achievements, controversies
        * GEOPOLITICS → countries, conflicts, diplomacy, strategy, economics
        * ECONOMICS → money, finance, market systems, trade, companies
        * PSYCHOLOGY → behavior, cognition, mental models, emotions
        * PHILOSOPHY → ideas, theories, ethics, abstract reasoning
        * TECHNOLOGY → software, AI, engineering, inventions, computing
        * SPORTS → players, teams, rivalries, events, tactical analysis
        * CRIME → investigations, incidents, criminal organizations, mysteries
        * MILITARY → weapons, tactics, wars, operations, defense systems
        * CULTURE → traditions, art, societal evolution, religions
        * MYSTERY → unexplained events, unsolved cases, unknown phenomena

        Also detect:

        1. Content style:

        * EXPLANATORY
        * NARRATIVE
        * TIMELINE
        * ANALYTICAL
        * COMPARATIVE
        * BREAKDOWN
        * CASE_STUDY

        2. Emotional tone:

        * SERIOUS
        * NEUTRAL
        * DARK
        * INSPIRING
        * TENSE
        * CURIOUS

        3. Complexity:

        * LOW
        * MEDIUM
        * HIGH

        Rules:

        * Output only structured JSON.
        * Do not explain your reasoning.
        * Do not generate script content.
        * Be precise.

        Topic:
        {topic}
    """
    )

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = IntentState
    )

    result = agent.invoke(
        {
            'messages':{
                'role':'user',
                'content': prompt
                }
        }
    )

    print(f"[Intent] {time.time()-st}")
    
    return {'intent': result['structured_response']}