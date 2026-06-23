import os
import time
from textwrap import dedent
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

class IntentState(BaseModel):
    intent: list[str]


load_dotenv()

model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

@tool('intent', description='This tool is for knowing intent behind the topic user entered', return_direct=False)
def intent(topic):
    
    system_prompt = dedent(
        f"""
        You are professional cognetive thinking agent.

        [TASK]
        Take the topic and think about it, then clearly and cognetively analyze the intent of the topic.
        """
    )

    prompt = dedent(
        f"""
        TOPIC
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
    result = result['structured_responses']
    return {'intent': result}