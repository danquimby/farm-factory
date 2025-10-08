from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime

from app.core.schemas import UserMixin
from app.features.building.schemas import BuildingDetails


class BuildingResourceSchema(BaseModel):
    level: int
    resource_id: int
    amount: int
    structure_id: int
    model_config = ConfigDict(from_attributes=True)
