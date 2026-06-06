"""Main entry point of the pipeline."""

import time

from langgraph.graph import StateGraph, START, END

from core.agents.plan import planner
from core.agents.research import researcher, fan_out_node
from core.agents.compile import compiler

from core.schemas.state import state

#===========================
# IMPORTS ↑
# ==========================

def ask():
    while True:
        topic = input("Enter Video Topic: ")
        if topic.strip() != "":
            return topic
        print("Topic cannot be empty. Please enter a valid topic.")

topic = ask()


#GRAPH

builder = StateGraph(state)

builder.add_node('perspective', planner)
builder.add_node('researcher', researcher)
builder.add_node('compiler', compiler)


builder.add_edge(START, 'perspective')
builder.add_conditional_edges('perspective', fan_out_node)
builder.add_edge('researcher', 'compiler')
builder.add_edge('compiler', END)


graph = builder.compile()

t = time.time()
result = graph.invoke(
    {
        "topic": topic,
        "domains": [],
        "perspectives": [],
        "summaries": [],
        "final_report": ""
    }
)
print('Total Agents Time: ', time.time() - t)
print(result)