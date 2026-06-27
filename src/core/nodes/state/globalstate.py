from typing import TypedDict, Annotated
import operator

from core.nodes.research.state.PlannerState import PlannerState
from core.nodes.script.state.ScriptWriter import ScriptState
from core.nodes.audio.state.AudioSegment import AudioSegment

class GlobalInformationState(TypedDict):
    topic: str
    information: list[PlannerState]
    script: ScriptState
    audio: Annotated[
        list[AudioSegment],
        operator.add
        ]
    timing: list[str]