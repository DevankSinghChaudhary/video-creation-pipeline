import os
import time
from dotenv import load_dotenv
from textwrap import dedent

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from core.nodes.grouping.state.grouping import groupingschema
from core.prompt import get_systemprompt 

load_dotenv()
model = ChatOpenAI(
    model = 'lightning-ai/gemma-4-31B-it',
    base_url = 'https://lightning.ai/api/v1/',
    api_key = os.getenv('OPENAI_API_KEYR')
)

system_prompt = get_systemprompt("grouper")

def groupingagent(state: dict) -> list:
    
    print(f'[GroupingAgent] Tool Called')
    st = time.time()

    script = state['script']

    prompt = dedent(f"""
    You are given a documentary narration script.

    Your task is to organize it into visually coherent display groups for typography rendering.

    Group the script in a way that each segment feels natural to read on screen.

    Focus on meaning continuity.

    Do not split phrases awkwardly.

    Do not split connected ideas just because of word count.

    Group by semantic flow, not fixed-size chunks.

    Rules:

    - Keep important phrase relationships together
    - Keep numbers and their units together
    - Keep percentages together
    - Keep names together
    - Keep dates together
    - Keep cause-effect connectors together
    - Remove commas, periods, semicolons, and colons from display text
    - Preserve question marks, exclamation marks, percentages, years, and abbreviations

    Preferred group size:
    2 to 5 words

    Allowed:
    1 to 7 words if required for natural flow

    Do not rewrite.
    Do not paraphrase.
    Do not summarize.
    Do not add or remove meaning.

    Return only strict JSON.

    Script:
    {script}
    """)


    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = groupingschema
    )

    result = agent.invoke(
        {
            'messages': {
                'role': 'user',
                'content': prompt
                }
        }
    )
    print(f'[GroupingAgent] {time.time()-st}')
    print(f'[GroupingAgent] Call Finish')
    
    return {'grouped': result['messages'][-1].content}