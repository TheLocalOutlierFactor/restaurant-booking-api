import pytest

from httpx import ASGITransport, AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.main import app
from src.database import get_async_session, Base
from src.config import (TEST_DATABASE_USER,
                        TEST_DATABASE_PASSWORD,
                        TEST_DATABASE_HOST,
                        TEST_DATABASE_PORT,
                        TEST_DATABASE_NAME)


TEST_DATABASE_URL = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
    user=TEST_DATABASE_USER,
    password=TEST_DATABASE_PASSWORD,
    host=TEST_DATABASE_HOST,
    port=TEST_DATABASE_PORT,
    name=TEST_DATABASE_NAME,
)


@pytest.fixture(name="engine")
async def engine_fixture():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(name="session")
async def session_fixture(engine):
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


@pytest.fixture(name="client")
async def client_fixture(session):
    async def get_session_override():
        return session

    app.dependency_overrides[get_async_session] = get_session_override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()
