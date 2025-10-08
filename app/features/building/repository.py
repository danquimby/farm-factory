from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository
from app.features.building.models import Building
from app.features.building.schemas import (
    CreateBuilding,
    BuildingDetails,
    CreateBuildingResponse,
    GetBuilding,
)
from app.exceptions.build_max_level import BuildingMaxLevelException
from app.exceptions.not_found_building import NotFoundBuildingException


class BuildingRepository(BaseRepository[Building]):
    def __init__(self, db: AsyncSession):
        super().__init__(Building, db)

    async def make(self, schema: CreateBuilding) -> CreateBuildingResponse:
        building = Building(
            x=schema.x,
            y=schema.y,
            level=0,
            structure_id=schema.structure_id,
            game_map_id=schema.game_map_id,
        )
        self.db.add(building)
        await self.db.commit()
        await self.db.refresh(building)
        return CreateBuildingResponse.model_validate(building)

    async def get_raw(self, schema: GetBuilding) -> Building | None:
        """
        Получаем модель строение + структура
        :param schema:
        :return: Building
        """
        query = (
            select(Building)
            .where(
                and_(
                    Building.x == schema.x,
                    Building.y == schema.y,
                    Building.game_map_id == schema.game_map_id,
                )
            )
            .options(selectinload(Building.structure))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get(self, schema: GetBuilding) -> BuildingDetails | None:
        if building := await self.get_raw(schema):
            return BuildingDetails.model_validate(building)
        return None

    async def level_up(self, schema: GetBuilding) -> Building:
        building = await self.get_raw(schema)
        if building:
            if building.level == building.structure.max_level:
                raise BuildingMaxLevelException(building.level + 1)
            return await self.update(building.id, level=building.level + 1)
        raise NotFoundBuildingException(schema.model_dump_json())
