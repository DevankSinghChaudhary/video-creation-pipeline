import os
import shutil
from core.nodes.state.globalstate import GlobalInformationState
from gradio_client import Client, handle_file
from langgraph.types import Send  


def FanoutScript(state: GlobalInformationState):
    return [
        Send(
            'Voice', {'script_for_tts': script}
        )
        for script in state['script'].script_ 
    ]

def Voice(state: GlobalInformationState):
    tts_client = Client('http://127.0.0.1:7860')
    
    scene_id = str(state["script_for_tts"].id)

    result = tts_client.predict(
        ref_audio_input=handle_file('D:/Projects/Applications/Video-Editing-Pipeline/src/core/nodes/audio/example.wav'),
        ref_text_input="But the real problem is that the waste heat from energy production at this scale would heat the Earth by over 20 degrees Celsius, which would make large parts of the planet.",
        gen_text_input=state['script_for_tts'].script,
        remove_silence=False,
        randomize_seed=False,
        seed_input=0,
        cross_fade_duration_slider=0.3,
        nfe_slider=64,
        speed_slider=1,
        api_name="/basic_tts"
        )
    
    temp_path = result[0]

    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)
    ext = os.path.splitext(temp_path)[1]

    final_destination = os.path.join(output_dir, f"scene_{scene_id}{ext}")
    
    shutil.move(temp_path, final_destination)

    return {
        'audio': [final_destination]
    }