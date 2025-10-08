from pydantic import BaseModel, ConfigDict, Field

from app.features.structure.schemas import StructureDetails


class GetBuilding(BaseModel):
    game_map_id: int
    x: int
    y: int


class UpgradeBuilding(BaseModel):
    structure_id: int


class BuildingResourceSchema(BaseModel):
    resource_id: int
    amount: int


class LevelUpBuilding(GetBuilding):
    building_resources: list[BuildingResourceSchema] | None = Field(
        default_factory=list
    )

class CreateBuilding(GetBuilding):
    structure_id: int
    building_resources: list[BuildingResourceSchema] | None = Field(
        default_factory=list
    )


class CreateBuildingResponse(BaseModel):
    id: int
    x: int
    y: int
    level: int
    model_config = ConfigDict(from_attributes=True)


class BuildingDetails(BaseModel):
    x: int
    y: int
    level: int
    structure: StructureDetails | None = None
    model_config = ConfigDict(from_attributes=True)
