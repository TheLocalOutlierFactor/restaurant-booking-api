import pytest

from datetime import datetime

from tests.test_table import create_table
from src.utils import exceptions

async def post_table(client, name="Столик 1", seats=2, location="Главный зал"):
    table = create_table(name, seats, location)
    response = await client.post("/tables/", json=table)

    created_id = response.json()["id"]
    return created_id


def create_reservation(table_id,
                       customer_name="Фасолин Геннадий Степанович",
                       reservation_time="2025-04-10T10:20",
                       duration_minutes=120):
    reservation = {
        "customer_name": customer_name,
        "table_id": table_id,
        "reservation_time": datetime.strptime(reservation_time, "%Y-%m-%dT%H:%M").isoformat(),
        "duration_minutes": duration_minutes
    }
    return reservation


@pytest.mark.asyncio
async def test_add_reservation(client):
    new_table_id = await post_table(client)
    reservation = create_reservation(table_id=new_table_id)

    response = await client.post("/reservations/", json=reservation)
    data = response.json()

    assert response.status_code == 201
    assert data["customer_name"] == reservation["customer_name"]
    assert data["table_id"] == reservation["table_id"]
    assert data["reservation_time"] == reservation["reservation_time"]
    assert data["duration_minutes"] == reservation["duration_minutes"]


@pytest.mark.asyncio
async def test_read_reservations(client):
    new_table_id = await post_table(client)

    reservation_1 = create_reservation(
        customer_name="Сорокина Анна Анатольевна",
        table_id=new_table_id,
        reservation_time="2025-04-12T18:00",
        duration_minutes=30
    )
    reservation_2 = create_reservation(
        customer_name="Бородач Степан Геннадиевич",
        table_id=new_table_id,
        reservation_time="2025-04-11T22:30",
        duration_minutes=60
    )

    await client.post("/reservations/", json=reservation_1)
    await client.post("/reservations/", json=reservation_2)

    response = await client.get("/reservations/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["customer_name"] == reservation_1["customer_name"]
    assert data[0]["table_id"] == reservation_1["table_id"]
    assert data[0]["reservation_time"] == reservation_1["reservation_time"]
    assert data[0]["duration_minutes"] == reservation_1["duration_minutes"]
    assert data[1]["customer_name"] == reservation_2["customer_name"]
    assert data[1]["table_id"] == reservation_2["table_id"]
    assert data[1]["reservation_time"] == reservation_2["reservation_time"]
    assert data[1]["duration_minutes"] == reservation_2["duration_minutes"]


@pytest.mark.asyncio
async def test_reservation_foreign_key_constraint(client):
    reservation = create_reservation(table_id=1)
    response = await client.post("/reservations/", json=reservation)

    assert response.status_code == 409
    assert response.json()["detail"] == exceptions.TABLE_NOT_FOUND


@pytest.mark.asyncio
async def test_reservation_conflict(client):
    new_table_id = await post_table(client)

    reservation_1 = create_reservation(
        customer_name="Горбушин Петр Леонидович",
        table_id=new_table_id,
        reservation_time="2025-04-11T18:00",
        duration_minutes=61  # Ends at 19:01
    )  # Should pass and serve as base for validation
    reservation_2 = create_reservation(
        customer_name="Певцова Любовь Павловна",
        table_id=new_table_id,
        reservation_time="2025-04-11T17:59",
        duration_minutes=30  # Ends at 18:29
    )  # Should raise error and do nothing because 18:29 (end) > 18:00 (existing reservation start)
    reservation_3 = create_reservation(
        customer_name="Барин Георгий Олегович",
        table_id=new_table_id,
        reservation_time="2025-04-11T19:00",
        duration_minutes=120  # Ends at 21:00
    )  # Should raise error and do nothing because 19:00 (start) < 19:01 (existing reservation end)
    reservation_4 = create_reservation(
        customer_name="Голубкина Дарья Андреевна",
        table_id=new_table_id,
        reservation_time="2025-04-11T17:00",
        duration_minutes=60  # Ends at 18:00
    )  # Should pass because 18:00 (end) == 18:00 (existing reservation start) and equality check is not strict
    reservation_5 = create_reservation(
        customer_name="Луков Семен Семенович",
        table_id=new_table_id,
        reservation_time="2025-04-11T19:05",
        duration_minutes=15  # Ends at 19:20
    )  # Should pass because 19:05 (start) > 19:01 (existing reservation end)

    response_1 = await client.post("/reservations/", json=reservation_1)
    response_2 = await client.post("/reservations/", json=reservation_2)
    response_3 = await client.post("/reservations/", json=reservation_3)
    response_4 = await client.post("/reservations/", json=reservation_4)
    response_5 = await client.post("/reservations/", json=reservation_5)

    assert response_1.status_code == 201
    assert response_2.status_code == 400
    assert response_2.json()["detail"] == exceptions.RESERVATION_CONFLICT
    assert response_3.status_code == 400
    assert response_3.json()["detail"] == exceptions.RESERVATION_CONFLICT
    assert response_4.status_code == 201
    assert response_5.status_code == 201


@pytest.mark.asyncio
async def test_remove_reservation(client):
    # DELETE method needs extra logic to check for ForeignKey constraints on delete
    pass
