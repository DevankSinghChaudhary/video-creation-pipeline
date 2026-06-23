import subprocess
import requests
import time



ASPECTRATIO = '9:16'


def start_tts_server():
    try:
        requests.get("http://127.0.0.1:7860", timeout=2)
        print("TTS already running.")
        return

    except:
        print("Starting TTS server...")

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "conda_hook & conda activate base & "
                "C:\\pinokio\\api\\e2-f5-tts.git\\app\\env\\Scripts\\activate "
                "C:\\pinokio\\api\\e2-f5-tts.git\\app\\env && "
                "f5-tts_infer-gradio"
            ],
            shell=True
        )

        # wait until server is live
        while True:
            try:
                requests.get("http://127.0.0.1:7860", timeout=2)
                print("TTS ready.")
                break
            except:
                time.sleep(2)