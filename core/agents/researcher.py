"""Defines the Researcher Agent which performs web research based on a given topic and prompt, utilizing specified tools for web search and date-time retrieval."""

from langchain.agents import create_agent

def researcher_agent(model, prompt: str, topic: str, ResearcherAgentOutput, search_web, get_current_date_time) -> str:
    agent = create_agent(
        model = model,
        tools = [search_web, get_current_date_time],
        system_prompt = f"You are professional researcher, research about the TOPIC: '{topic}' gracefully. Fully understand the topic first, then create multiple query to search web and then tool call each query single handly. REMOVE KEYWORDS FROM WEB INFO LIKE: 'Instagram', 'Twitter', 'Facebook', 'LinkedIn', 'Reddit', 'YouTube', 'Wikipedia', 'Google', 'Bing', 'DuckDuckGo', 'Yahoo' and other keywords that are not relevant to the topic. Don't include the keywords in the final summary. Just use them for searching the web. After getting all the information from web, create a informative summary about the topic. Don't include any irrelevant information in the summary, just include the relevant information about the topic.",
        response_format = ResearcherAgentOutput
        )
    result  = agent.invoke({
        'messages':[{
            'role': 'user',
            'content': prompt
        }]
    })
    return result