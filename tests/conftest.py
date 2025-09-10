import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.orm import Base
from app.transport.depends.db import get_async_session
from app.utils.settings import EnvSettings


@pytest.fixture(scope='session')
def fix_env_settings():
    return EnvSettings(test_postgres_dsn='postgresql+asyncpg://testuser:testpassword@localhost:5432/vinyltestdb')

@pytest_asyncio.fixture(scope='session')
async def async_engine(fix_env_settings):
    engine = create_async_engine(
        fix_env_settings.test_postgres_dsn,
        echo=False,
        poolclass=NullPool,
    )
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session", autouse= True)
async def create_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_session(async_engine):
    async_session_maker = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_engine.connect() as connection:
        trans = await connection.begin()
        async with async_session_maker(bind=connection) as session:
            yield session
        await trans.rollback()

@pytest_asyncio.fixture
async def client(async_session):
    async def override_get_async_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
