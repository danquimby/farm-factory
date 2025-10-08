from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime

from app.core.schemas import UserMixin
from app.features.building.schemas import BuildingDetails


class GameMapDetailsWithoutBuildings(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)

class GameMapDetails(GameMapDetailsWithoutBuildings):
    buildings: list | None = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class GameMapCreate(UserMixin):
    name: str
