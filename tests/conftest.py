import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import settings
from database import get_session, Base
from main import app


test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)

test_async_session_maker = sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:

    async with test_async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
