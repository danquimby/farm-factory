from fastapi import APIRouter, Depends, status

from app.features.auth.models import User
from app.features.dependencies import get_game_map_service, get_current_user
from app.features.game_map.schemas import GameMapCreate, GameMapDetails, GameMapDetailsWithoutBuildings
from app.services.game_map_service import GameMapService

router = APIRouter(prefix="/game_map", tags=["game_map"])


@router.post(
    "/make", response_model=GameMapDetailsWithoutBuildings | None, status_code=status.HTTP_201_CREATED
)
async def create_map(
    game_map: GameMapCreate,
    current_user: User = Depends(get_current_user),
    game_map_service: GameMapService = Depends(get_game_map_service),
):
    # todo не нравиться, потом как нить сделать миксин
    game_map.user_id = current_user.id
    result = await game_map_service.create(game_map)
    return GameMapDetailsWithoutBuildings.model_validate(result)


# отдаем всю карту с данными обьектов
@router.get("/game_map", response_model=list[GameMapDetails])
async def get_game_map(
    game_map_id: int,
    # current_user: User = Depends(get_current_user),
    game_map_service: GameMapService = Depends(get_game_map_service),
):
    return await game_map_service.get_by_id(game_map_id)
