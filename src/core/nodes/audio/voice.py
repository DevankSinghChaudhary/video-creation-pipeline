import os
import shutil
import time
from core.nodes.state.globalstate import GlobalInformationState
from gradio_client import Client, handle_file
from langgraph.types import Send  
from pathlib import Path

path = './src/core/nodes/audio/output/'

try:
    shutil.rmtree(path)
except: 
    pass

def FanoutScript(state: GlobalInformationState):
    return [
        Send(
            'Voice', {'script_for_tts': script}
        )
        for script in state['script'].script_ 
    ]



def Voice(state: GlobalInformationState):
    tts_client = Client("http://127.0.0.1:7860")
    s = time.time()
    
    scene_id = str(state["script_for_tts"].id)

    result = tts_client.predict(
        ref_audio_input=handle_file('D:/Projects/Applications/Video-Editing-Pipeline/src/core/nodes/audio/example.mp3'),
        ref_text_input="From the earliest days of history man have grappled a problem yet it is only within two hundred years for aircraft and one hundered for submarines.",
        gen_text_input=state['script_for_tts'].script,
        remove_silence=False,
        randomize_seed=False,
        seed_input=0,
        cross_fade_duration_slider=0.15,
        nfe_slider=64,
        speed_slider=1.0,
        api_name="/basic_tts"
        )
    
    temp_path = result[0]


    os.makedirs(path, exist_ok=True)
    ext = os.path.splitext(temp_path)[1]

    final_destination = os.path.join(path, f"{scene_id}{ext}")
    
    shutil.move(temp_path, final_destination)

    print(f"TTS: {time.time()-s}")
    return {
        'audio': [final_destination]
    }