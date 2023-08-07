import pytest


async def test_get_courses_not_found(client):
    response = client.get(url="/courses/")

    assert response.status_code == 404
