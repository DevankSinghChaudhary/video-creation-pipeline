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

    output_path = r"D:\Projects\Applications\Video-Editing-Pipeline\src\core\video-rendering\public\voice.mp3"

    combined.export(output_path, format="mp3")

    print(f"Merger: {time.time()-s}")

    return {"audio": [output_path]}