import urllib.parse

import pytest
from sqlalchemy import select

from users.models import User
from users.repository import UserRepo
from users.services import UserService


async def test_create_user(clear_tables, client, async_session):
    user_data = {
        "name": "Danial",
        "surname": "Bidaibek",
        "email": "bid@gmail.com",
        "password": "123",
        "role": "STUDENT"
    }

    response = client.post(url="/users/", json=user_data)

    data_from_resp = response.json()

    assert response.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp['role'] == user_data['role']

    user_from_db = await async_session.execute(
        select(User).where(User.email == user_data['email'])
    )

    assert len(user_from_db.all()) == 1


async def test_create_user_validation_error(drop_tables, client):
    user_data = {
        "name": "Danial",
        "surname": "Bidaibek",
        "email": "bid@gmailcom",
        "password": "123",
        "role": "STUDENT"
    }

    response = client.post(url="/users/", json=user_data)

    assert response.status_code == 422
