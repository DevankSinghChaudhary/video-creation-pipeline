"""Main entry point of the pipeline."""
import time

from langgraph.graph import StateGraph, START, END

from core.nodes.state.globalstate import GlobalInformationState 
from core.nodes.research.agent.plan import planner
from core.nodes.research.agent.script import writer
from core.nodes.director.agent.illustrator import illustrator
from core.nodes.director.agent.director import director
from core.nodes.layout.layoutplanner import layoutplanner

from core.user import user_input

def main(state: GlobalInformationState):
    
    st = time.time()

    builder = StateGraph(state)

    builder.add_node('planner', planner)
    builder.add_node('writer', writer)
    builder.add_node('illustrator', illustrator)
    builder.add_node('director', director)
    builder.add_node('layout', layoutplanner)

    builder.add_edge(START, 'planner')
    builder.add_edge('planner', 'writer')
    builder.add_edge('writer', 'illustrator')
    builder.add_edge('illustrator', 'director')
    builder.add_edge('director', 'layout')
    builder.add_edge('layout', END)

    graph = builder.compile()

    topic = user_input()
    result = graph.invoke({
        'topic': topic,
        'information': [],
        'script': [],
        'visual': [],
        'layout': []
        })
    print(f'Total Time: {time.time()-st}')
    return result


if __name__ == "__main__":
    print(main(GlobalInformationState))
