import subprocess
from core.nodes.state.globalstate import GlobalInformationState
from gradio_client import client, handle_file


def voice(state: GlobalInformationState):
    script = state['script']

    subprocess.Popen(
        [
            r"C:\pinokio\api\e2-f5-tts.git\app\env\Scripts\f5-tts_infer-gradio.exe"
        ],
        cwd=r"C:\pinokio\api\e2-f5-tts.git\app"
    )

    tts_client = client('http://127.0.0.1:7860')
    for scripts in scripts:
        tts_client.predict(script.script_breakdown)
