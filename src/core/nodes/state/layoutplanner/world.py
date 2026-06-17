from pydantic import BaseModel


class ScenePlacement(BaseModel):
    scene_id: int

    world_x: float
    world_y: float
    world_z: float

class worldstate(BaseModel):
    scene_positions: list[ScenePlacement]
