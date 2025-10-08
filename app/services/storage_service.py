from loguru import logger
from starlette import status

from app.core.exceptions import HTTPException
from app.features.storage.models import Storage
from app.features.storage.repository import StorageRepository, ResourceRepository
from app.features.storage.schemas import (
    CreateDefaultStorage,
    ActionStorage,
    ActionStorageResponse,
)


class StorageService:
    storage_repository: StorageRepository
    resource_repository: ResourceRepository

    def __init__(
        self,
        storage_repository: StorageRepository,
        resource_repository: ResourceRepository,
    ):
        self.storage_repository = storage_repository
        self.resource_repository = resource_repository

    async def do_action(self, schema: ActionStorage):
        try:
            resource = await self.resource_repository.get_by_id(schema.resource_id)
            if resource is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"not found resource_id: {schema.resource_id}",
                )

            if schema.action == "take":
                result: Storage = await self.storage_repository.take(
                    schema.game_map_id, schema.resource_id, schema.value
                )
                return ActionStorageResponse(
                    game_map_id=schema.game_map_id,
                    resource_id=schema.resource_id,
                    new_value=result.value,
                )
            elif schema.action == "add":
                result: Storage = await self.storage_repository.add(
                    schema.game_map_id, schema.resource_id, schema.value
                )
                return ActionStorageResponse(
                    game_map_id=schema.game_map_id,
                    resource_id=schema.resource_id,
                    new_value=result.value,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"incorrect action:{schema.action}",
                )
        except Exception as e:
            import traceback

            logger.error(traceback.format_exc())
            raise e

    async def create_default(self, schema: CreateDefaultStorage):
        resources = await self.resource_repository.get_all()
        await self.storage_repository.create_default(schema.game_map_id, resources)
