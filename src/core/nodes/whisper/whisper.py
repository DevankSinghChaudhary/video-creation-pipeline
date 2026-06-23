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

    print(result.stdout)
    print(result.stderr)

    output = result.stdout.strip().splitlines()[-1]
    
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("WhisperX failed")

    output = result.stdout.strip()

    json_start = output.find("[")
    output = output[json_start:]
    print(f'Whisper: {time.time()-st}')
    return {"timing": json.loads(output)}