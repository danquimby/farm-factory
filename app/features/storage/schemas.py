from typing import Literal
from pydantic import BaseModel, ConfigDict


class ActionStorageResponse(BaseModel):
    game_map_id: int
    resource_id: int
    new_value: int


class ActionStorage(BaseModel):
    game_map_id: int
    action: Literal["take", "add"]
    resource_id: int
    value: int


class MultipleChangeAmountItem(BaseModel):
    resource_id: int
    amount: int


class CreateDefaultStorage(BaseModel):
    game_map_id: int
