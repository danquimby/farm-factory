from typing import Generic, TypeVar, Type, List, Any

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
C = TypeVar("C", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: int) -> T | None:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 300) -> List[T]:
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in: C) -> T:
        db_obj = self.model(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: int, **kwargs) -> T | None:
        result = await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(delete(self.model).where(self.model.id == id))
        await self.db.commit()
        return result.rowcount > 0

    async def exists(self, **filters: Any) -> bool:
        stmt = select(self.model).filter_by(**filters)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None
