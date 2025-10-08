from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.core.exceptions import HTTPException
from app.features.dependencies import (
    get_storage_service,
)
from app.features.storage.schemas import CreateDefaultStorage, ActionStorage, ActionStorageResponse
from app.services.storage_service import StorageService

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/make", status_code=HTTP_200_OK)
async def make_default_storage(
    schema: CreateDefaultStorage,
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
    # current_user: User = Depends(get_current_user)
):
    try:
        return await storage_service.create_default(schema)
    except Exception as e:
        import traceback
        print(traceback.print_exc())
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/add", status_code=HTTP_200_OK, response_model=ActionStorageResponse)
async def add_resource(
    schema: ActionStorage,
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
    # current_user: User = Depends(get_current_user)
):
    try:
        return await storage_service.do_action(schema)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))




@router.post("/take", status_code=HTTP_200_OK, response_model=ActionStorageResponse)
async def take_resource(
    schema: ActionStorage,
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
    # current_user: User = Depends(get_current_user)
):
    try:
        return await storage_service.do_action(schema)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
