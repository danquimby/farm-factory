from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository
from app.features.game_map.models import GameMap
from app.features.structure.models import Structure


# Добавление и удаление только через миграции
class StructureRepository(BaseRepository[Structure]):
    def __init__(self, db: AsyncSession):
        super().__init__(Structure, db)

