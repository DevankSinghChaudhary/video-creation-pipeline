"""Main entry point of the pipeline."""
import time

from langgraph.graph import StateGraph, START, END

from core.nodes.state.globalstate import GlobalInformationState 
from core.nodes.research.plan import Planner
from core.nodes.script.script import Writer
from core.nodes.script.formatter import Formatter
from core.nodes.audio.voice import Voice, FanoutScript
from core.nodes.director.agent.illustrator import Illustrator
from core.nodes.director.agent.director import Director
from core.nodes.layout.layoutplanner import Layoutplanner
from core.nodes.layout.worldlayout import Worldplanner

from core.user import user_input




def main(state: GlobalInformationState):
    

    builder = StateGraph(state)

    builder.add_node('Planner', Planner)
    builder.add_node('Writer', Writer)
    builder.add_node('Voice', Voice)
    builder.add_node('Formatter',Formatter)

    builder.add_edge(START, 'Planner')
    builder.add_edge('Planner', 'Writer')
    builder.add_edge('Writer', 'Formatter')
    builder.add_conditional_edges('Formatter', FanoutScript)
    builder.add_edge('Voice', END)

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
    print(state)