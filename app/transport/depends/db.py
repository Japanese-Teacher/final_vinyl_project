from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from app.utils.settings import get_env_settings


def get_async_engine() -> AsyncEngine:
    return create_async_engine(get_env_settings().postgres_dsn)

def get_async_session_maker(
        async_engine: Annotated[AsyncEngine, Depends(get_async_engine)],
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

async def get_async_session(
        session_maker: Annotated[async_sessionmaker, Depends(get_async_session_maker)],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise