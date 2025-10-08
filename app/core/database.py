from time import sleep
from loguru import logger
from sqlalchemy import Column, Integer, DateTime, text
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator

from .config import settings

# Create async engine
async_engine = create_async_engine(
    settings.db.db_url,
    echo=True,
    pool_pre_ping=True,
    # echo_pool="debug",
    pool_size=2,
    max_overflow=0,
    connect_args={
        "timeout": 10,
        "server_settings": {"jit": "off"},
    },
    future=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Base class for models
DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Dependency to get async DB session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session dependency for FastAPI.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_tables():
    """
    Create all tables in the database asynchronously.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    """
    Drop all tables in the database asynchronously.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def check_db() -> bool:
    for _ in range(10):
        try:
            logger.info(f"check database {settings.db.db_url}")
            async with async_engine.begin() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception as ex:
            logger.info(f"check exception {ex=}")
            sleep(4)
    return False
