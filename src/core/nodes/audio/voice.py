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
    result = tts_client.predict(
        ref_audio_input=handle_file('D:/Projects/Applications/Video-Editing-Pipeline/src/core/nodes/audio/example.wav'),
        ref_text_input="But the real problem is that the waste heat from energy production at this scale would heat the Earth by over 20 degrees Celsius, which would make large parts of the planet.",
        gen_text_input=state['script_for_tts'].script,
        remove_silence=False,
        randomize_seed=True,
        seed_input=0,
        cross_fade_duration_slider=0.15,
        nfe_slider=32,
        speed_slider=1.2,
        api_name="/basic_tts"
        )
    return {
        'audio': [result[0]]
    }