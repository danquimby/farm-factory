from fastapi import APIRouter

from app.features.auth.routes import router as auth_router
from app.features.game_map.routes import router as game_map_router
from app.features.structure.routes import router as structure_router
from app.features.building.routes import router as building_router
from app.features.storage.routes import router as storage_router
from app.core.routes import router as core_routes

all_routers = APIRouter(
    prefix='/api/v1',
)

all_routers.include_router(auth_router)
all_routers.include_router(game_map_router)
all_routers.include_router(structure_router)
all_routers.include_router(building_router)
all_routers.include_router(storage_router)

core_routers = APIRouter(
    prefix='',
)
core_routers.include_router(core_routes)
