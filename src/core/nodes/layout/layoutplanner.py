import os
import time
from dotenv import load_dotenv
from textwrap import dedent

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.globalstate import GlobalInformationState
from core.nodes.state.layoutplanner.state import layoutstate
from core.constant import ASPECTRATIO

from core.prompt import get_systemprompt

load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt('layoutplanner')

def layoutplanner(state: GlobalInformationState):
    topic = state['topic']
    script  = state['script']


    prompt = dedent(
        f"""
        # Topic

        {topic}

        # Narration Script

        {script}

        # Aspect Ratio

        {ASPECTRATIO}

        ---

        Create a spatial layout plan for the documentary.

        Determine:

        - Which assets belong together.
        - Which assets are primary, secondary, and supporting.
        - How assets should be grouped into scenes.
        - Relative x, y, and z positioning.
        - Information hierarchy.
        - Logical spatial relationships between assets.

        Use the narration flow to organize the layout.

        The layout must be optimized for the provided aspect ratio.

        The goal is to create an information space that can later be used by camera and motion planning systems.

        Return only data matching the schema.
        """
    )

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = layoutstate 
    )
    st = time.time()
    result = agent.invoke({
        'messages':{
            'role':'user',
            'content': prompt
        }
    })
    print(f'Layout Planner: {time.time()-st}')
    result = result['structured_response']

    return {
        'layout': result
    }