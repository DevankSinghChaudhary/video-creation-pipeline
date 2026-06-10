from langgraph.graph import StateGraph, START, END

from core.nodes.state.research.plannerstate import GlobalInformationState
from core.nodes.research.agent.plan import planner
from core.nodes.research.agent.script import writer
from core.nodes.research.agent.visual import Illustrator

from core.user import user_input


import time
def research_node(state: GlobalInformationState):
    builder = StateGraph(state)

    builder.add_node('planner', planner)
    builder.add_node('writer', writer)
    builder.add_node('illustrator', Illustrator)

    builder.add_edge(START, 'planner')
    builder.add_edge('planner', 'writer')
    builder.add_edge('writer', 'illustrator')
    builder.add_edge('illustrator', END)

    graph = builder.compile()

    
    topic = user_input()
    
    starttime = time.time()
    result = graph.invoke(
        {
            'topic': topic,
            'information': [],
            'script': [],
            'visual': []
        }
    )
    print('Total Time: ', time.time() - starttime)
    return result


output = research_node(GlobalInformationState)
print(output)