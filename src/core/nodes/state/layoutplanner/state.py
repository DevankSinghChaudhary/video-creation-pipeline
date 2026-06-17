from pydantic import BaseModel

class Asset(BaseModel):
    name: str
    role: str
    purpose: str

class SceneAsset(BaseModel):
    asset: Asset
    x: float
    y: float
    z: float

class SceneLayout(BaseModel):
    scene_id: int
    title: str
    width: float
    height: float
    assets: list[SceneAsset]

class layoutstate(BaseModel):
    scenes: list[SceneLayout]