import pytest


@pytest.mark.asyncio
async def test_create_table(client):
    response = await client.post("/tables/", json={
        "name": "Столик 1",
        "seats": 2,
        "location": "У камина"
    })
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Столик 1"
    assert data["seats"] == 2
    assert data["location"] == "У камина"
