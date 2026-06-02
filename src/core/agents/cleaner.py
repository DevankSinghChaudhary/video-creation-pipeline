"""Defines the cleaner agent which takes structured input and cleans the formatting while preserving the structure."""

from langchain.agents import create_agent

from core.schemas.cleaner import CleanerAgentOutput

def cleaner_agent(model: str, prompt: str, CleanerAgentOutput: CleanerAgentOutput) -> CleanerAgentOutput:
    """"Structured output for the cleaner agent."""
    agent =create_agent(
        model = model,
        system_prompt = "You are provided with structured input but you have to clean all the formatting from it, not in sense of structure but formatting like: REMOVE THESE('/n', '\n', '\n\n','\\n', '\\t','\\\\n', extra spaces, etc). Keep Bolding, Italic type formatting. Just clean the text and give me the cleaned version of the text. Don't change the structure of the text, just clean the formatting.",
        response_format = CleanerAgentOutput
        )
    
    result = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    
    return result