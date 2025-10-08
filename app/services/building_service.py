from app.core.exceptions import HTTPException
from app.features.building.repository import BuildingRepository
from app.features.building.schemas import (
    CreateBuilding,
    GetBuilding,
    BuildingDetails,
    BuildingResourceSchema,
    LevelUpBuilding,
)
from app.features.building_resource.repository import BuildingResourceRepository
from app.exceptions.build_max_level import BuildingMaxLevelException
from app.exceptions.not_found_building import NotFoundBuildingException
from app.exceptions.requirements import (
    NotEnoughException,
    ExtraResourcesException,
)
from app.features.storage.repository import StorageRepository
from app.features.storage.schemas import MultipleChangeAmountItem


class BuildingService:
    building_repository: BuildingRepository
    building_resource_repository: BuildingResourceRepository

    def __init__(
        self,
        building_repository: BuildingRepository,
        building_resource_repository: BuildingResourceRepository,
        storage_repository: StorageRepository,
    ):
        self.building_repository = building_repository
        self.building_resource_repository = building_resource_repository
        self.storage_repository = storage_repository

    # todo нужна транзакция на бд, но пока я еще не понял как лучше это сделать
    async def make(self, schema: CreateBuilding):
        if result := await self.building_repository.get(
            GetBuilding(
                x=schema.x,
                y=schema.y,
                game_map_id=schema.game_map_id,
            )
        ):
            raise Exception(f"exist building {result=}")

        try:
            # проверяем наличие ресурсов для 0 уровня,
            # если не находим значит не нужно ресурсов
            await self.check_requirements(
                schema.structure_id, schema.building_resources, 0
            )
            await self.storage_repository.take_multiple(
                schema.game_map_id,
                [
                    MultipleChangeAmountItem.model_validate(req.model_dump())
                    for req in schema.building_resources
                ],
            )
            return await self.building_repository.make(schema)
        except (NotEnoughException, ExtraResourcesException) as e:
            raise HTTPException(422, str(e))
        except Exception as ex:
            import traceback

            raise HTTPException(500, traceback.format_exc())

    async def get(self, schema: GetBuilding) -> BuildingDetails | None:
        return await self.building_repository.get(schema)

    async def level_up(self, schema: LevelUpBuilding):
        """Делаем подьем обьекта и проверка на его максимум"""
        try:

            building = await self.building_repository.get_raw(
                GetBuilding(**schema.model_dump(exclude={"building_resources"}))
            )
            await self.check_requirements(
                building.structure_id, schema.building_resources, 0
            )
            result = await self.building_repository.level_up(
                GetBuilding.model_validate(schema)
            )
            return result.level
        except (
            NotEnoughException,
            NotFoundBuildingException,
            BuildingMaxLevelException,
        ) as e:
            raise HTTPException(422, detail=str(e))
        except Exception as e:
            raise HTTPException(500, detail=e)

    async def check_requirements(
        self,
        structure_id: int,
        building_resources: list[BuildingResourceSchema],
        level: int,
    ):
        """
        Проверяем если есть требования, что они все выполнены
        :return:
        """
        requirements = await self.building_resource_repository.get_requirements(
            structure_id, level
        )
        if requirements:
            # Есть требования

            building_resources_set = {
                (o.resource_id, o.amount) for o in building_resources
            }
            requirements_set = {(o.resource_id, o.amount) for o in requirements}
            need_resource = requirements_set - building_resources_set
            if need_resource:
                raise NotEnoughException(need_resource)
        elif building_resources:
            raise ExtraResourcesException(
                {(o.resource_id, o.amount) for o in building_resources}
            )
