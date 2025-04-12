import pytest

from datetime import datetime
from tests.test_table import create_table


async def post_table(client, name="Столик 1", seats=2, location="главный зал"):
    table = create_table(name, seats, location)
    response = await client.post("/tables/", json=table)

    created_id = response.json()["id"]
    return created_id


def create_reservation(customer_name="Геннадий Степанович",
                       table_id=1,
                       reservation_time="2025-04-10T10:20",
                       duration_minutes=120):
    reservation = {
        "customer_name": customer_name,
        "table_id": table_id,
        "reservation_time": datetime.strptime(reservation_time, "%Y-%m-%dT%H:%M").isoformat(),
        "duration_minutes":duration_minutes
    }
    return reservation


@pytest.mark.asyncio
async def test_create_reservation(client):
    new_table_id = await post_table(client)
    reservation = create_reservation(table_id=new_table_id)

    response = await client.post("/reservations/", json=reservation)
    data = response.json()

    assert response.status_code == 201
    assert data["customer_name"] == reservation["customer_name"]
    assert data["table_id"] == reservation["table_id"]
    assert data["reservation_time"] == reservation["reservation_time"]
    assert data["duration_minutes"] == reservation["duration_minutes"]
