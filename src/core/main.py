"""Main entry point of the pipeline."""

from pydantic import BaseModel
from textwrap import dedent
import json
import time

from langgraph.graph import StateGraph, START, END

from core.agents.perspective import perspective_agent
from core.agents.cleaner import cleaner_agent
from core.agents.researcher import researcher_agent

#===========================
# IMPORTS ↑
# ==========================

# STATE CLASS
class state(BaseModel):
    topic: str
    primary_domain: list[str]
    secondary_domain: list[str]
    perspective: list[str]
    summary: str

def ask():
    while True:
        topic = input("Enter Video Topic: ")
        if topic.strip() != "":
            return {'topic': topic}
        print("Topic cannot be empty. Please enter a valid topic.")

topic = ask()

#===========================
# USER INPUT ↑ 
# ==========================

#----------------------------------------------------------------------------------------------------------------------------------------


#=================================================================================
#                           PERSPECTIVE AGENT
#=================================================================================

tp = time.time()
system_prompt = dedent(f"""
Topic: {topic}.
TASK: Generate ResearchPlan for documentary.
FORMAT: strict schema only.
STYLE: documentary explainer.
DOMAIN: auto-infer.
OUTPUT: no explanation.
""")

prompt = dedent(f"""
Analyze this topic: '{topic}, create domains and perspective.'""")
perspectiveagent = perspective_agent(prompt, system_prompt)
print('Perspective: ', time.time() - tp)


tr = time.time()
#=================================================================================
#                           RESEARCHER AGENT
#=================================================================================
system_prompt = dedent(f"""
Topic: {topic}.
TASK: Generate summary of topic.
FORMAT: strict schema only.
STYLE: documentary explainer.
DOMAIN: auto-infer.
INPUT: DATA THAT SHOULD BE USED TO CREATE QUERIES IF NEEDED
OUTPUT: no explanation.
EXTRA: SEARCH IN DOMAIN AND SUBDOMAIN (NOT AS PASSED)
EXAMPLE: 'Us-Iran conflict', 'Us-Iran war impacts' etc [Purely example no relation with user topic]
USE TOOLS REASONABLY.
""")

prompt = dedent(f"""
Analyze this topic: '{topic}', create create summary about the topic.

Data:
{perspectiveagent}
""")
research_agent = researcher_agent(prompt, system_prompt)
print('Researcher: ', time.time() - tr)


#=================================================================================
#                           CLEANER AGENT
#=================================================================================
tc = time.time()
system_prompt = dedent(f"""
TASK: Remove all formatting.
Fomatting_example: '\\n', 'n', '\\', '\\\\' etc 
""")

system_prompt = dedent(f"""
DATA: {research_agent}""")

cleaner_output = cleaner_agent(prompt, system_prompt)
print('Cleaner: ', time.time() - tc)
print('==================/n')

print(cleaner_output)


graph = StateGraph()
graph.add_node()