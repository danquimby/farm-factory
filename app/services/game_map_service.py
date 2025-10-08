from typing import List

from loguru import logger

from app.core.exceptions import HTTPException
from app.features.game_map.models import GameMap
from app.features.game_map.repository import GameMapRepository
from app.features.game_map.schemas import GameMapCreate, GameMapDetails


class GameMapService:
    game_map_repository: GameMapRepository

    def __init__(self, game_map_repository: GameMapRepository):
        self.game_map_repository = game_map_repository

    async def get_by_id(self, id: int) -> list[GameMapDetails]:
        if result := await self.game_map_repository.get_data_by_id(id):
            return result
        raise HTTPException(404, f'not found game_map: {id}' )

    async def create(self, schema: GameMapCreate) -> GameMap:
        return await self.game_map_repository.create(schema)

    async def delete(self, id: int) -> bool:
        logger.info(f'incoming delete {id=} ')
        # todo пока думаю сделать флаг, а не удалять запись
        return True
