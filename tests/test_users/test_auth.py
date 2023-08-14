import uuid


async def test_authentication(client, create_user_in_database):
    id = uuid.uuid4()
    user_data = {
        "id": id,
        "name": "Danial",
        "surname": "Bidaibek",
        "email": "auth_test@gmail.com",
        "password": "123",
        "is_active": True,
        "role": "STUDENT"
    }

    await create_user_in_database(**user_data)

    response = client.post("/users/token/", json={"username": user_data['email'], "password": "123"})

    assert response.status_code == 200
