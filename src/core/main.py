"""Main entry point of the pipeline."""
import time
import os

from langgraph.graph import StateGraph, START, END

from core.nodes.state.globalstate import GlobalInformationState 
from core.nodes.research.agent.plan import Researcher
from core.nodes.script.agent.script import Writer
from core.nodes.grouping.agent.grouping import groupingagent
from core.nodes.script.agent.formatter import Formatter
from core.nodes.audio.voice import Voice, FanoutScript
from core.nodes.audio.merger import MergeAudio
from core.nodes.whisper.whisper import Timing
from core.nodes.renderer.renderer import Renderer
from core.user import user_input


def main(state: GlobalInformationState):
    
    scene_path = r'D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering\src\scene.json'
    mp3_path = r'D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering\public\voice.mp3'
    video_path = r'D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering\out\video.mp4'

    for path in [scene_path, mp3_path, video_path]:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass


    builder = StateGraph(state)

    builder.add_node('Researcher', Researcher)
    builder.add_node('Writer', Writer)
    builder.add_node('Grouper', groupingagent)
    builder.add_node('Voice', Voice)
    builder.add_node('Formatter',Formatter)
    builder.add_node('MergeAudio', MergeAudio)
    builder.add_node('Timing', Timing)
    builder.add_node('Renderer', Renderer)

    builder.add_edge(START, 'Researcher')
    builder.add_edge('Researcher', 'Writer')
    builder.add_edge('Writer', 'Formatter')
    builder.add_edge('Writer', 'Grouper')
    builder.add_conditional_edges('Formatter', FanoutScript)
    builder.add_edge('Voice', 'MergeAudio')
    builder.add_edge('MergeAudio', 'Timing')
    builder.add_edge(['Grouper', 'Timing'], 'Renderer')
    builder.add_edge('Renderer', END)

    graph = builder.compile()

    st = time.time()
    result = graph.invoke({
        'topic': user_input(),
        'information': [],
        'script': [],
        'timing': [],
        'grouped': []
        })
    
    print(f'Total Time: {time.time()-st}')
    return result

if __name__ == "__main__":
    state = main(GlobalInformationState)
    print(state['grouped'])