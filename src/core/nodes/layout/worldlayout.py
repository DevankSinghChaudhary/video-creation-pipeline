import os
import time
from dotenv import load_dotenv
from textwrap import dedent

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.globalstate import GlobalInformationState
from core.nodes.state.layoutplanner.world import worldstate
from core.prompt import get_systemprompt
from core.constant import ASPECTRATIO


load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)
system_prompt = get_systemprompt('worldplanner')



def Worldplanner(state: GlobalInformationState):
    topic = state['topic']
    visuals = state['visual']
    information = state['information']
    script = state['script']
    layout = state['layout']

    prompt = dedent(
    f"""
    # Topic

    {topic}

    # Research Information

    {information}

    # Narration Script

    {script}

    # Visuals

    {visuals}
    
    # Director Scenes

    {layout}

    # Aspect Ratio

    {ASPECTRATIO}

    ---

    Create a world-space layout for the documentary.

    Arrange all scenes into a single continuous documentary world.

    Determine:

    * Global position of each scene.
    * Relative distance between scenes.
    * Spatial relationships between scenes.
    * Logical narrative progression through world space.
    * Grouping of related scenes.
    * Separation of unrelated scenes.
    * Navigation-friendly scene placement.

    Preserve all scene layouts exactly as provided.

    Do not modify:

    * Scene contents.
    * Asset positions inside scenes.
    * Visual hierarchy.
    * Narration flow.

    Focus only on positioning scenes within a shared world coordinate system.

    Optimize for:

    * Future camera navigation.
    * Smooth transitions between scenes.
    * Clear narrative progression.
    * Efficient world traversal.
    * Readable spatial organization.

    The world should feel intentionally designed rather than randomly arranged.

    Return only data matching the schema.
    """
    )


    agent = create_agent(
        model = model, 
        system_prompt = system_prompt,
        response_format = worldstate
    )

    result = agent.invoke({
        'messages':{
            'role':'user',
            'content':prompt
        }
    })
    result = result['structured_response']

    return {
        'worldscene': result
    }