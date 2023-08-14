import uuid

import pytest

from users.models import RoleEnum, User


async def test_get_user_by_id(client, create_user_in_database):
    id = uuid.uuid4()
    user_data = {
        "id": id,
        "name": "Danial",
        "surname": "Bidaibek",
        "email": "dan@gmail.com",
        "password": "123",
        "is_active": True,
        "role": "STUDENT"
    }

    await create_user_in_database(**user_data)

    response = client.get(f'/users/{id}/')

    assert response.status_code == 200
