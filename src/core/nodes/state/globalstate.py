from typing import TypedDict

from core.nodes.state.director.state import DirectorState
from core.nodes.state.research.state import PlannerState
from core.nodes.state.research.state import ScriptState
from core.nodes.state.layoutplanner.state import layoutstate


class GlobalInformationState(TypedDict):
    topic: str
    information: list[PlannerState]
    script: ScriptState
    visual: DirectorState
    layout: layoutstate