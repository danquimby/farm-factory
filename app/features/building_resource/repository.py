from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.features.building.models import Building
from app.features.building_resource.models import BuildingResource
from app.features.building_resource.schemas import BuildingResourceSchema


class BuildingResourceRepository(BaseRepository[BuildingResource]):
    def __init__(self, db: AsyncSession):
        super().__init__(Building, db)

    async def get_requirements(
        self, structure_id: int, level: int
    ) -> list[BuildingResourceSchema]:
        query = select(BuildingResource).where(
            and_(
                BuildingResource.structure_id == structure_id,
                BuildingResource.level == level,
            )
        )
        result = await self.db.execute(query)
        records = result.scalars()
        return [BuildingResourceSchema.model_validate(record) for record in records]

    async def check(self, data):
        """Проверяем хватает ли всего"""
        pass
