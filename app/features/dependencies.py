from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.features.auth.models import User, RefreshToken
from app.features.auth.repository import UserRepository, RefreshTokenRepository
from app.features.building.repository import BuildingRepository
from app.features.building_resource.repository import BuildingResourceRepository
from app.features.game_map.repository import GameMapRepository
from app.features.storage.repository import StorageRepository, ResourceRepository
from app.features.structure.repository import StructureRepository
from app.services.building_service import BuildingService
from app.services.game_map_service import GameMapService
from app.services.storage_service import StorageService
from app.services.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="JWT")


def get_building_resource_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> BuildingResourceRepository:
    return BuildingResourceRepository(session)

def get_resource_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> ResourceRepository:
    return ResourceRepository(session)


def get_storage_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> StorageRepository:
    return StorageRepository(session)


def get_struct_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> StructureRepository:
    return StructureRepository(session)


def get_build_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> BuildingRepository:
    return BuildingRepository(session)


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> UserRepository:
    return UserRepository(session)


def get_refresh_token_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


def get_game_map_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> GameMapRepository:
    return GameMapRepository(session)


def get_building_service(
    game_map_repository: Annotated[BuildingRepository, Depends(get_build_repository)],
    building_resource_repository: Annotated[BuildingResourceRepository, Depends(get_building_resource_repository)],
    storage_repository: Annotated[StorageRepository, Depends(get_storage_repository)],
) -> BuildingService:
    return BuildingService(game_map_repository, building_resource_repository, storage_repository)


def get_game_map_service(
    game_map_repository: Annotated[GameMapRepository, Depends(get_game_map_repository)],
) -> GameMapService:
    return GameMapService(game_map_repository)


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    token_repository: Annotated[RefreshToken, Depends(get_refresh_token_repository)],
) -> UserService:
    return UserService(user_repository, token_repository)


def get_storage_service(
    storage_repository: Annotated[StorageRepository, Depends(get_storage_repository)],
    resource_repository: Annotated[ResourceRepository, Depends(get_resource_repository)],
) -> StorageService:
    return StorageService(storage_repository, resource_repository)


async def get_current_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    token: str = Depends(oauth2_scheme),
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user := await user_service.get_current_user(token):
        return user
    raise credentials_exception
