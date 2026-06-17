"""Main entry point of the pipeline."""
import time

from langgraph.graph import StateGraph, START, END

from core.nodes.state.globalstate import GlobalInformationState 
from core.nodes.research.agent.plan import planner
from core.nodes.research.agent.script import writer
from core.nodes.director.agent.illustrator import illustrator
from core.nodes.director.agent.director import director
from core.nodes.layout.layoutplanner import layoutplanner
from core.nodes.layout.worldlayout import worldplanner

from core.user import user_input

def main(state: GlobalInformationState):
    

    builder = StateGraph(state)

    builder.add_node('planner', planner)
    builder.add_node('writer', writer)


    builder.add_edge(START, 'planner')
    builder.add_edge('planner', 'writer')
    builder.add_edge('writer', END)

    graph = builder.compile()

    topic = user_input()
    st = time.time()
    result = graph.invoke({
        'topic': topic,
        'information': [],
        'script': []
        })
    
    print(f'Total Time: {time.time()-st}')
    return result


if __name__ == "__main__":
    state = main(GlobalInformationState)
    for scene in state["script"].script_:
        print(scene.script)
        print()
        print()