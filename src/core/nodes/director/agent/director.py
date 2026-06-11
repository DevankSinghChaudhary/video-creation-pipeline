import os
import time
from dotenv import load_dotenv
from textwrap import dedent

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.globalstate import GlobalInformationState
from core.nodes.state.director.state import DirectorState
from core.prompt import get_systemprompt

load_dotenv()
model = ChatOpenAI(
    model = 'mistral-medium-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt("director")

def director(state: GlobalInformationState):
    topic = state['topic']
    script = state['script']
    visuals = state['visual']
    information = state['information']


    prompt = dedent(
        f"""
       TOPIC:
        {topic}

        RESEARCH INFORMATION:
        {information}

        NARRATION SCRIPT:
        {script}

        VISUAL CONCEPTS:
        {visuals}

        TASK:

        Analyze the narration script and available visual concepts.

        Your goal is to transform the visual concepts into a small number of coherent documentary scenes.

        A scene is a group of visuals that together communicate one primary idea from the narration.

        Focus on:

        * What the audience should understand.
        * Which visuals belong together.
        * Which visuals are unnecessary.
        * How information should be grouped.
        * How scenes should progress logically through the narration.

        Use the narration as the primary source of truth.

        Research information may be used only when necessary to better understand the script.

        Visual concepts are raw material, not final scenes.

        You may remove visual concepts that do not improve understanding.

        You may combine multiple visual concepts into a single scene.

        For a 30-40 second documentary:

        * Prefer 3-6 scenes.
        * Prefer fewer, stronger scenes.
        * Avoid fragmentation.
        * Avoid visual overload.
        * Avoid one visual per scene.

        For each scene determine:

        * Title
        * Purpose
        * Supported narration segment
        * Visuals included

        Every scene should communicate exactly one primary idea.

        Do not create scenes for side stories.

        Do not introduce new facts.

        Do not introduce new topics.

        Do not create scenes that are decorative.

        Do not generate camera movements.

        Do not generate animation instructions.

        Do not generate image prompts.

        Do not generate video prompts.

        Return only data matching the output schema.
        """
    )


    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = DirectorState
    )
    t = time.time()
    result = agent.invoke({
        'messages':{
            'role':'user',
            'content': prompt
        }
    })
    print("Director: ", time.time()-t)
    result = result['structured_response']
    return {
        'visual': result
    }