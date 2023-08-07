import asyncio
import os
import sys
import uuid
from typing import Any, Generator, AsyncGenerator

import asyncpg
import pytest
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NotSupportedError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)
from users.models import User, RoleEnum
import settings
from database import get_session, Base, async_session
from main import app
from users.services import _AuthenticationService


engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)

# Create the session factory
async_session_tmp = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_session():

    async with async_session_tmp() as session:
        yield session
        # Rollback changes and close the session at the end of each test
        await session.rollback()
        await session.close()


async def _create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _drop_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            settings.TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        async with test_engine.begin() as connection:
            async_session = sessionmaker(
                bind=connection, expire_on_commit=False, class_=AsyncSession
            )
            await _drop_tables(test_engine)
            await _create_tables(test_engine)
            async with async_session() as session:
                yield session
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_session] = _get_test_db
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.pop(get_session)


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    await pool.close()


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        id: str,
        name: str,
        surname: str,
        email: str,
        is_active: bool,
        password: str,
        role: str
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO "user" VALUES ($1, $2, $3, $4, $5, $6, $7);""",
                id,
                name,
                surname,
                email,
                is_active,
                password,
                role
            )

    return create_user_in_database


# @pytest.fixture(scope="function")
# async def user(async_session):
#     user_data = {
#         "id": uuid.uuid4(),
#         "name": "Danial",
#         "surname": "Bidaibek",
#         "email": "danial@gmail.com",
#         "password": "123",
#         "is_active": True,
#         "role": RoleEnum.STUDENT
#     }
#
#     # Create a new user record in the database
#     user = User(**user_data)
#     async_session.add(user)
#     await async_session.commit()
#     yield user
#     #
#     # try:
#     #     async with async_session.begin() as conn:
#     #         query = select(User).where(User.email == user_data["email"])
#     #         result = await async_session.execute(query)
#     #         user = result.scalar_one_or_none()
#     #
#     #         yield user
#     # except NotSupportedError as e:
#     #     async_session.close()
#     #     async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#     #     async_session = async_session()
#     #     raise e



