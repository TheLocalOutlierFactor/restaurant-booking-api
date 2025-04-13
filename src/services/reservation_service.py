from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast
from sqlalchemy.dialects.postgresql import INTERVAL

from src.models.reservation import Reservation
from src.models.table import Table
from src.schemas.reservation import ReservationCreate
from src.utils import exceptions


async def get_all_reservations(db: AsyncSession):
    result = await db.execute(select(Reservation))
    return result.scalars().all()


async def table_exists(db: AsyncSession, table_id: int):
    result = await db.execute(select(Table).where(Table.id == table_id))
    return bool(result.scalars().first())


async def is_reserved(db: AsyncSession, table_id: int, start_time: datetime, duration: int):
    end_time = start_time + timedelta(minutes=duration)

    interval_expression = cast(Reservation.duration_minutes.op("||")(" minutes"), INTERVAL)
    reserved = await db.execute(select(Reservation).where(
        (Reservation.table_id == table_id) &
        (Reservation.reservation_time < end_time) &
        ((Reservation.reservation_time + interval_expression) > start_time)
    ))
    return bool(reserved.scalars().first())


async def create_reservation(db: AsyncSession, reservation: ReservationCreate):
    table_found = await table_exists(db, reservation.table_id)
    if not table_found:
        raise exceptions.ForeignKeyError()

    reserved = await is_reserved(
        db,
        reservation.table_id,
        reservation.reservation_time,
        reservation.duration_minutes
    )
    if reserved:
        raise exceptions.ReservationConflictError()

    db_res = Reservation(**reservation.model_dump())
    db.add(db_res)
    await db.commit()
    await db.refresh(db_res)
    return db_res


async def delete_reservation(db: AsyncSession, reservation_id: int):
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    db_res = result.scalars().first()
    if db_res:
        await db.delete(db_res)
        await db.commit()
    return db_res
