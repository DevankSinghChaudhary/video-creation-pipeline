import os
import time
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.research.state import ScriptState
from core.nodes.state.globalstate import GlobalInformationState
from core.prompt import get_systemprompt

load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt("writer")

def writer(state: GlobalInformationState):
    topic = state['topic']
    information = state['information']


    prompt = f"""
    You are an elite documentary scriptwriter.

    TOPIC:
    {topic}

    TASK:
    Write a compelling documentary-style narration script using ONLY the information provided.

    GOAL:
    Create a script suitable for a 30-40 second short-form documentary video.

    INFORMATION:
    {information}

    RULES:

    * Use only information from the provided research.
    * Never invent facts, dates, statistics, quotes, or events.
    * Prioritize the most important and interesting information.
    * Focus on one clear narrative.
    * Every sentence must provide new information.
    * Avoid repetition.
    * Avoid filler phrases.
    * Do not include introductions, greetings, or calls to action.
    * Do not mention sources.
    * Do not use bullet points.
    * Do not use headings.
    * Do not include scene descriptions.
    * Do not include camera instructions.
    * Do not include timestamps.

    STYLE:

    * Documentary narrator.
    * Concise and information-dense.
    * Clear and engaging.
    * Professional and authoritative.
    * Build curiosity and momentum.
    * Use active voice whenever possible.
    * Make complex topics understandable to a general audience.

    STRUCTURE:

    1. Start with the most surprising, important, or impactful fact.
    2. Explain the key development, event, or mechanism.
    3. End with the broader significance, consequence, or implication.

    LENGTH:

    * Target 90-120 words.
    * Maximum 140 words.

    OUTPUT:
    Return only the final narration script.
    """

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = ScriptState
    )
    
    t = time.time()
    result = agent.invoke({
        'messages':{
            'role':'user',
            'content': prompt
        }
    })
    print('Writer: ', time.time() - t)
    result = result['structured_response']
    return {
        'script': result
    }