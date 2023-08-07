import uuid

import pytest

from users.models import RoleEnum, User


async def test_get_user_by_id(client, asyncpg_pool):
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
                """INSERT INTO "user" VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                id,
                name,
                surname,
                email,
                is_active,
                password,
                role
            )

    await create_user_in_database(**user_data)

    response = client.get(f'/users/{id}/')

    assert response.status_code == 200
