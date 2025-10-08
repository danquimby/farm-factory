import traceback
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from app.core.exceptions import HTTPException
from app.features.auth.models import User
from app.features.auth.schemas import (
    UserResponse,
)
from app.features.building.schemas import (
    CreateBuilding,
    CreateBuildingResponse,
    GetBuilding,
    BuildingDetails, LevelUpBuilding,
)
from app.features.dependencies import (
    get_current_user,
    get_building_service,
)
from loguru import logger
from app.services.building_service import BuildingService

router = APIRouter(prefix="/building", tags=["building"])


@router.post(
    "/create", status_code=HTTP_201_CREATED, response_model=CreateBuildingResponse
)
async def create_new_building(
    schema: CreateBuilding,
    game_map_service: Annotated[BuildingService, Depends(get_building_service)],
    # current_user: User = Depends(get_current_user)
):
    try:
        return await game_map_service.make(schema)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/get", status_code=HTTP_201_CREATED, response_model=BuildingDetails)
async def get_building_by_position(
    game_map_service: Annotated[BuildingService, Depends(get_building_service)],
    schema: GetBuilding = Depends(),
    # current_user: User = Depends(get_current_user)
):
    try:
        return await game_map_service.get(schema)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=409, detail=str(e))


# наверное эти события нужны только закрытые
@router.delete("/destroy", response_model=UserResponse)
async def building_destroy(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/level_up", status_code=201)
async def building_level_up(
    schema: LevelUpBuilding,
    game_map_service: Annotated[BuildingService, Depends(get_building_service)],
):
    try:
        new_level = await game_map_service.level_up(schema)
        return f"level up success {new_level=}"
    except Exception as e:
        logger.error(traceback.print_exc())
        raise HTTPException(status_code=409, detail=str(e))

