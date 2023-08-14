import pytest
from httpx import AsyncClient
from sqlalchemy import select, insert
from starlette.datastructures import FormData

from tests.conftest import test_async_session_maker
from users.models import User


async def user_by_email(user_email: str):
    async with test_async_session_maker() as session:
        query = select(User).where(User.email == user_email)
        result = await session.execute(query)
        user = result.all()
        return user


class TestUser:
    async def test_register(self, ac: AsyncClient):
        user_data = {
            "name": "Testname",
            "surname": "Testsurname",
            "email": "test_email@gmail.com",
            "password": "test",
        }

        response = await ac.post("/users/", json=user_data)
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == user_data["name"]
        assert data["surname"] == user_data["surname"]
        assert data["email"] == user_data["email"]

        user = await user_by_email(user_data["email"])

        assert len(user) == 1

    async def test_register_validation_error(self, ac: AsyncClient):
        user_data = {
            "name": "Testname",
            "surname": "Testsurname",
            "email": "test_email2gmail.com",
            "password": "test",
        }

        response = await ac.post("/users/", json=user_data)

        assert response.status_code == 422
        user = await user_by_email(user_data["email"])

        assert len(user) == 0

    async def test_auth(self, ac: AsyncClient):
        form_data = FormData({"username": "test_email@gmail.com", "password": "test"})
        response = await ac.post("/users/token/", data=form_data)

        data = response.json()

        assert response.status_code == 200
        assert isinstance(data['access_token'], str)
        assert len(data['access_token']) > 0
        assert data['type'] == 'bearer'

    async def test_auth_email_error(self, ac: AsyncClient):
        form_data = FormData({"username": "test_emai@gmail.com", "password": "test"})
        response = await ac.post("/users/token/", data=form_data)

        data = response.json()

        assert response.status_code == 400
        assert data['detail'] == "Incorrect email or password"

    async def test_auth_password_error(self, ac: AsyncClient):
        form_data = FormData({"username": "test_email@gmail.com", "password": "test1"})
        response = await ac.post("/users/token/", data=form_data)

        data = response.json()

        assert response.status_code == 400
        assert data['detail'] == "Incorrect email or password"
