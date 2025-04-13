import pytest

from src.utils import exceptions


def create_table(name="Столик 1", seats=2, location="Главный зал"):
    table = {
        "name": name,
        "seats": seats,
        "location": location,
    }
    return table


@pytest.mark.asyncio
async def test_add_table(client):
    table = create_table()

    response = await client.post("/tables/", json=table)
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == table["name"]
    assert data["seats"] == table["seats"]
    assert data["location"] == table["location"]


@pytest.mark.asyncio
async def test_read_tables(client):
    table_1 = create_table(
        name="Столик 1",
        seats=2,
        location="Главный зал"
    )
    table_2 = create_table(
        name="Столик 2",
        seats=4,
        location="Терраса"
    )

    await client.post("/tables/", json=table_1)
    await client.post("/tables/", json=table_2)

    response = await client.get("/tables/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == table_1["name"]
    assert data[0]["seats"] == table_1["seats"]
    assert data[0]["location"] == table_1["location"]
    assert data[1]["name"] == table_2["name"]
    assert data[1]["seats"] == table_2["seats"]
    assert data[1]["location"] == table_2["location"]


@pytest.mark.asyncio
async def test_table_unique_constrain(client):
    table_1 = create_table(name="Столик 1", seats=2, location="Главный зал")
    table_2 = create_table(name="Столик 1", seats=4, location="Терраса")

    response_success = await client.post("/tables/", json=table_1)
    response_clash = await client.post("/tables/", json=table_2)

    assert response_success.status_code == 201
    assert response_clash.status_code == 409
    assert response_clash.json()["detail"] == exceptions.TABLE_ALREADY_EXISTS


@pytest.mark.asyncio
async def test_remove_table(client):
    table_1 = create_table(name="Столик 1", seats=2, location="Главный зал")
    table_2 = create_table(name="Столик 2", seats=4, location="Терраса")

    create_table_1_response = await client.post("/tables/", json=table_1)
    create_table_2_response = await client.post("/tables/", json=table_2)

    created_table_1_id = create_table_1_response.json()["id"]
    created_table_2_id = create_table_2_response.json()["id"]

    delete_table_1_response = await client.delete(f"/tables/{created_table_1_id}")
    delete_table_2_response = await client.delete(f"/tables/{created_table_2_id}")
    delete_missing_table_response = await client.delete(f"/tables/{created_table_1_id}")

    assert delete_table_1_response.status_code == 200
    assert delete_table_2_response.status_code == 200
    assert delete_missing_table_response.status_code == 404
