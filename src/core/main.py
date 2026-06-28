"""Main entry point of the pipeline."""
import time
import json
import os
import shutil
import subprocess

from langgraph.graph import StateGraph, START, END

from core.nodes.state.globalstate import GlobalInformationState 
from core.nodes.research.agent.plan import Planner
from core.nodes.script.agent.script import Writer
from core.nodes.script.agent.formatter import Formatter
from core.nodes.audio.voice import Voice, FanoutScript
from core.nodes.audio.merger import MergeAudio
from core.nodes.whisper.whisper import Timing
from core.nodes.renderer.renderer import Renderer
from core.user import user_input


def main(state: GlobalInformationState):
    
    scene_path = r'D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering\src\scene.json'

    try:
        if os.path.exists(scene_path):
            os.remove(scene_path)
    except Exception:
        pass

    builder = StateGraph(state)

    builder.add_node('Planner', Planner)
    builder.add_node('Writer', Writer)
    builder.add_node('Voice', Voice)
    builder.add_node('Formatter',Formatter)
    builder.add_node('MergeAudio', MergeAudio)
    builder.add_node('Timing', Timing)
    builder.add_node('Renderer', Renderer)

    builder.add_edge(START, 'Planner')
    builder.add_edge('Planner', 'Writer')
    builder.add_edge('Writer', 'Formatter')
    builder.add_conditional_edges('Formatter', FanoutScript)
    builder.add_edge('Voice', 'MergeAudio')
    builder.add_edge('MergeAudio', 'Timing')
    builder.add_edge('Timing', 'Renderer')
    builder.add_edge('Renderer', END)

    graph = builder.compile()

    topic = user_input()
    st = time.time()
    result = graph.invoke({
        'topic': topic,
        'information': [],
        'script': [],
        'timing': []
        })
    
    print(f'Total Time: {time.time()-st}')
    return result

if __name__ == "__main__":
    state = main(GlobalInformationState)
    print(state)