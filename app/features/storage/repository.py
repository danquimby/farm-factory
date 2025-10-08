from sqlalchemy import update, and_, case, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.exceptions.storage_negative import StorageNegativeException
from app.features.storage.models import Resource, Storage
from app.features.storage.schemas import MultipleChangeAmountItem


class ResourceRepository(BaseRepository[Resource]):
    def __init__(self, db: AsyncSession):
        super().__init__(Resource, db)


class StorageRepository(BaseRepository[Storage]):
    def __init__(self, db: AsyncSession):
        super().__init__(Resource, db)

    async def take_multiple(
        self, game_map_id: int, resources: list[MultipleChangeAmountItem]
    ):
        if not resources:
            return []

        # Создаем условия для каждого ресурса
        conditions = []
        for resource in resources:
            conditions.append(
                and_(
                    Storage.game_map_id == game_map_id,
                    Storage.resource_id == resource.resource_id,
                )
            )

        # Объединяем условия через OR
        where_condition = or_(*conditions)

        # Создаем CASE выражения для каждого ресурса
        # todo это плохо что мы не чего не уменьшаем, потом что то придумать нужно
        case_expressions = {}
        for resource in resources:
            case_expressions[resource.resource_id] = case(
                (Storage.value - resource.amount >= 0, Storage.value - resource.amount),
                else_=Storage.value,
            )

        # Обновляем значения
        query = (
            update(Storage)
            .where(where_condition)
            .values(
                value=case(
                    *[
                        (Storage.resource_id == resource_id, case_expr)
                        for resource_id, case_expr in case_expressions.items()
                    ],
                    else_=Storage.value,
                )
            )
            .returning(Storage)
        )

        result = await self.db.execute(query)
        updated_records = result.scalars().all()

        await self.db.commit()
        return updated_records

    async def take(self, game_map_id: int, resource_id: int, value: int):
        old_value = (
            await self.db.execute(
                select(Storage.value).where(
                    and_(
                        Storage.game_map_id == game_map_id,
                        Storage.resource_id == resource_id,
                    )
                )
            )
        ).scalar_one_or_none()
        if old_value is None:
            raise Exception(f"not Found {game_map_id=} {resource_id=}")
        query = (
            update(Storage)
            .where(
                and_(
                    Storage.game_map_id == game_map_id,
                    Storage.resource_id == resource_id,
                )
            )
            .values(
                value=case(
                    (Storage.value - value >= 0, Storage.value - value),
                    else_=Storage.value,
                )
            )
            .returning(Storage)
        )
        result: Storage = (await self.db.execute(query)).scalar_one()
        await self.db.commit()
        if result.value != old_value:
            return result
        raise StorageNegativeException(result.value, value)

    async def add(self, game_map_id: int, resource_id: int, value: int) -> Storage:
        old_value = (
            await self.db.execute(
                select(Storage.value).where(
                    and_(
                        Storage.game_map_id == game_map_id,
                        Storage.resource_id == resource_id,
                    )
                )
            )
        ).scalar_one_or_none()
        if old_value is None:
            raise Exception(f"not Found {game_map_id=} {resource_id=}")

        query = (
            update(Storage)
            .where(
                and_(
                    Storage.game_map_id == game_map_id,
                    Storage.resource_id == resource_id,
                )
            )
            .values(value=Storage.value + value)
            .returning(Storage)
        )
        return (await self.db.execute(query)).scalar_one()

    async def create_default(self, game_map_id: int, resources: list[Resource]):
        items: list[Storage] = []
        for resource in resources:
            storage_record = Storage(
                game_map_id=game_map_id, resource_id=resource.id, value=10
            )
            self.db.add(storage_record)
            items.append(storage_record)

        await self.db.commit()
