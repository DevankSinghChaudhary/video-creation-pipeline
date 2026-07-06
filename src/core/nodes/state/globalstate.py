import operator
from typing import TypedDict, Annotated

from core.nodes.research.state.PlannerState import PlannerState
from core.nodes.script.state.ScriptWriter import ScriptState
from core.nodes.audio.state.AudioSegment import AudioSegment
from core.nodes.grouping.state.grouping import groupingschema

class GlobalInformationState(TypedDict):
    topic: str
    information: list[PlannerState]
    script: ScriptState
    audio: Annotated[
        list[AudioSegment],
        operator.add
        ]
    timing: list[str]
    grouped: groupingschema