# tests/conftest.py

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.database import Base
from app.main import create_app

app = create_app()

# Тестовая база данных
TEST_DATABASE_URL = settings.db.test_db_url

@pytest_asyncio.fixture(scope="session")
async def async_engine():
    """Create async engine for tests."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )

    # Создаем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def async_session(async_engine):
    """Create async session for tests."""
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="session")
async def override_get_async_session(async_session):
    """Override dependency for FastAPI."""

    async def _override_get_async_session():
        yield async_session

    return _override_get_async_session
