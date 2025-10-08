from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

from app.core.schemas import UserMixin


class StructureDetails(BaseModel):
    id: int

    icon: str
    name: str
    image: str
    w: int
    h: int
    max_level: int
    enable: bool
    created_at: datetime
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)
