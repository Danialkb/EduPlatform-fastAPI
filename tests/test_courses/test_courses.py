import uuid

import pytest
from fastapi import Depends
from httpx import AsyncClient
from passlib.context import CryptContext
from sqlalchemy import insert, select, delete

from courses.dependencies import get_course_service
from courses.models import Course
from courses.services import CourseService
from tests.conftest import test_async_session_maker
from users.models import User
from utils.unit_of_work import UnitOfWork


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
async def clear_users():
    async with test_async_session_maker() as session:
        query = delete(Course)
        await session.execute(query)
        await session.commit()
        query = delete(User).where(User.email == "test@gmail.com")
        await session.execute(query)
        await session.commit()


@pytest.fixture()
async def courses(user):
    async with test_async_session_maker() as session:
        # course_list = []
        for i in range(1, 4):
            query = insert(Course).values(
                title=f"title{i}",
                owner_id=user.id
            )

            await session.execute(query)
            await session.commit()
            # course_list.append(res.scalar_one())


@pytest.fixture
async def course(user):
    async with test_async_session_maker() as session:
        query = insert(Course).values(
            title=f"title",
            owner_id=user.id
        ).returning(Course)
        res = await session.execute(query)
        await session.commit()

        return res.scalar_one()


@pytest.mark.usefixtures("clear_users")
class TestCourse:
    async def test_get_courses_error(self, ac: AsyncClient):
        response = await ac.get("/courses/")

        assert response.status_code == 404

    async def test_get_courses(self, ac: AsyncClient, courses):
        response = await ac.get("/courses/")

        assert response.status_code == 200

    async def test_get_course_error(self, ac: AsyncClient):
        response = await ac.get(f"/courses/{uuid.uuid4()}/")

        assert response.status_code == 404

    async def test_get_course(self, ac: AsyncClient, course):
        response = await ac.get(f"/courses/{course.id}/")

        data = response.json()

        assert response.status_code == 200
        assert data['title'] == course.title
        assert data['description'] == course.description
        assert data['owner']['id'] == str(course.owner_id)

    # async def test_edit_course(self, ac: AsyncClient, course):
    #     async with test_async_session_maker() as session:
    #         course_service = CourseService(UnitOfWork(session))
    #         edited = await course_service.edit_course(
    #             id=course.id,
    #             description="some description",
    #             logo=None,
    #             categories=["Data Science"]
    #         )
    #
    #         assert edited.description == "some description"
    #         assert edited.id == course.id
