from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config import (DATABASE_USER,
                        DATABASE_PASSWORD,
                        DATABASE_HOST,
                        DATABASE_PORT,
                        DATABASE_NAME)


DATABASE_URL = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    name=DATABASE_NAME,
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker  = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
