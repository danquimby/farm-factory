from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository
from app.features.building.models import Building
from app.features.game_map.models import GameMap
from app.features.game_map.schemas import GameMapDetails


class GameMapRepository(BaseRepository[GameMap]):
    def __init__(self, db: AsyncSession):
        super().__init__(GameMap, db)

    async def get_data_by_id(self, game_map_id: int) -> list[GameMapDetails] | None:
        query = (
            select(GameMap)
            .where(GameMap.id == game_map_id)
            .options(selectinload(GameMap.buildings).selectinload(Building.structure))
        )
        result = await self.db.execute(query)
        if game_maps := result.scalars().all():
            return [GameMapDetails.model_validate(game_map) for game_map in game_maps]
