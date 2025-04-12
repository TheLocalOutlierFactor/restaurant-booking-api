from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.reservation import Reservation
from src.schemas.reservation import ReservationCreate


async def get_all_reservations(db: AsyncSession):
    result = await db.execute(select(Reservation))
    return result.scalars().all()


async def is_reserved(db: AsyncSession, table_id: int, start_time, duration):
    end_time = start_time + timedelta(minutes=duration)
    reserved = await db.execute(select(Reservation).where(
        (Reservation.table_id == table_id) &
        (Reservation.reservation_time < end_time) &
        ((Reservation.reservation_time + timedelta(minutes=duration)) > start_time)
    ))
    return bool(reserved.scalars().first())


async def create_reservation(db: AsyncSession, reservation: ReservationCreate):
    reserved = await is_reserved(db,
                                 reservation.table_id,
                                 reservation.reservation_time,
                                 reservation.duration_minutes)
    if reserved:
        raise ValueError("Table is already reserved for this time.")
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
