""""Information Extraction Agent that uses web search and date-time to retrieve information about a topic."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from dotenv import load_dotenv
import os
