import os
import time
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.research.state import FormatterState
from core.nodes.state.globalstate import GlobalInformationState
from core.prompt import get_systemprompt

load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt("formatter")

def Formatter(state: GlobalInformationState):
    script = state['script']


    prompt = f"""
    You will receive documentary narration.

    Your task is to optimize it ONLY for natural TTS delivery.

    INPUT SCRIPT:
    {script}

    TASK:

    Reformat the script for speech synthesis.

    IMPORTANT:

    - Preserve ALL meaning exactly.
    - Preserve ALL facts, names, dates, and numbers.
    - Do NOT add new information.
    - Do NOT remove information.
    - Do NOT change sequence of events.
    - Do NOT rewrite for creativity.

    STRICT PAUSE RULES:

    - Never place pauses between grammatically connected words.
    - Never split subject and verb.
    - Never split verb and object.
    - Never split names, dates, or statistics.
    - Never use ellipses unless the pause is intentional and natural.
    - If unsure, use a period instead.
    - Grammar always has priority over dramatic pacing.

    OPTIMIZATION GOALS:

    - Add punctuation where needed for natural pauses.
    - Convert awkward line breaks into spoken rhythm.
    - Break long dense sentences into smaller speakable units.
    - Merge overly fragmented short lines if they sound unnatural.
    - Improve breathing rhythm.
    - Improve prosody.
    - Improve emphasis using punctuation only.
    - Improve pacing for documentary narration.
    - Make the output sound human when read by TTS.

    PACING RULES:

    - Use periods for major pauses.
    - Use commas for smaller pauses.
    - Use ellipses (...) for dramatic heavier pauses.
    - Use em dashes (—) for sharp interruptions or transitions.
    - Avoid run-on sentences.
    - Avoid over-fragmentation.
    - Avoid robotic clause stacking.

    GOAL:

    The final output should sound like a professional documentary narrator speaking naturally.

    OUTPUT:

    Return only the final formatted narration.
    """

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = FormatterState
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