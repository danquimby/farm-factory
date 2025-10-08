from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.core.database import check_db
from app.features import all_routers, core_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db()
    # startup
    logger.info("startup")
    yield
    # shutdown
    logger.info("shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        summary="Тестовый проект, который решает задачи с событиями",
        title="Farm project",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Authorization", "X-Project-ID", "X-Project-Name", "*"],
    )
    app.include_router(core_routers)
    app.include_router(all_routers)

    return app
