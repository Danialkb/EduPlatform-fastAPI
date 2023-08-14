
import pytest
from httpx import AsyncClient
from passlib.context import CryptContext
from sqlalchemy import insert, select

from courses.models import Course
from tests.conftest import test_async_session_maker
from users.models import User


@pytest.fixture
async def user():
    async with test_async_session_maker() as session:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        query = insert(User).values(
            name="test",
            surname="test",
            email="test@gmail.com",
            password=password_context.hash("123"),
        ).returning(User)
        user = await session.execute(query)
        await session.commit()
        yield user.scalar_one()



@pytest.fixture
async def courses(user):
    async with test_async_session_maker() as session:
        for i in range(1, 4):
            query = insert(Course).values(
                title=f"title{i}",
                owner_id=user.id
            )
            await session.execute(query)
            await session.commit()


class TestCourse:
    async def test_get_courses_error(self, ac: AsyncClient):
        response = await ac.get("/courses/")

        assert response.status_code == 404

    async def test_get_courses(self, ac: AsyncClient, courses):
        response = await ac.get("/courses/")

        assert response.status_code == 200
