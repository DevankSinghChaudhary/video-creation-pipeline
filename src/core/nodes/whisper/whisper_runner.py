# pyright: reportMissingImports=false
import whisperx
import json
import sys

audio_path = sys.argv[1]

model = whisperx.load_model("small", "cuda")
result = model.transcribe(audio_path)

model_a, metadata = whisperx.load_align_model(
    language_code=result["language"],
    device="cuda"
)

aligned = whisperx.align(
    result["segments"],
    model_a,
    metadata,
    audio_path,
    "cuda"
)
print(json.dumps(aligned["word_segments"]))