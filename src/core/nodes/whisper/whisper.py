import os
import json
import time
import subprocess

def Timing(state):
    audio_path = state['audio'][-1]
    st = time.time()

    result = subprocess.run(
        [
            r".whisperx\Scripts\python.exe",
            "src/core/nodes/whisper/whisper_runner.py",
            str(audio_path)
        ],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip().splitlines()[-1]
    
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("WhisperX failed")

    output = result.stdout.strip()

    json_start = output.find("[")
    output = output[json_start:]
    print(f'Whisper: {time.time()-st}')

    scene_path = r'D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering\src\scene.json'
    temp_path = scene_path + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(json.loads(output), file, indent=2)

    os.replace(temp_path, scene_path)

    return {"timing": json.loads(output)}