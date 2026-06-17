from typing import TypedDict, Annotated
import operator

from core.nodes.state.director.state import DirectorState
from core.nodes.state.research.state import PlannerState
from core.nodes.state.research.state import ScriptState
from core.nodes.state.layoutplanner.state import layoutstate
from core.nodes.state.layoutplanner.world import worldstate
from core.nodes.state.audio.state import AudioSegment


class GlobalInformationState(TypedDict):
    topic: str
    information: list[PlannerState]
    script: ScriptState
    audio: Annotated[
        list[AudioSegment],
        operator.add
        ]