import os
import time
from pydub import AudioSegment
from core.nodes.state.globalstate import GlobalInformationState


def MergeAudio(state: GlobalInformationState):
    
    s = time.time()

    combined = AudioSegment.empty()

    sorted_audio = sorted(
        state["audio"],
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0])
    )

    for file in sorted_audio:
        combined += AudioSegment.from_wav(file)

    combined.export("./src/core/nodes/audio/output/final.wav", format="wav")

    print(f'Merger: {time.time()-s}')

    return {"audio": ["./src/core/nodes/audio/output/final.wav"]}