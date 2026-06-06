from langgraph.graph import StateGraph, START, END

from core.schemas.state import state
from core.agents.plan import planner
from core.agents.research import researcher, fan_out_node
from core.agents.compile import compiler

from core.main import ask

builder = StateGraph(state)

builder.add_node('perspective', planner)
builder.add_node('researcher', researcher)
builder.add_node('compiler', compiler)


builder.add_edge(START, 'perspective')
builder.add_conditional_edges('perspective', fan_out_node)
builder.add_edge('researcher', 'compiler')
builder.add_edge('compiler', END)


graph = builder.compile()

topic = ask()
graph.invoke({
    'topic': topic,
    'domains': [],
    'research_results': []
})