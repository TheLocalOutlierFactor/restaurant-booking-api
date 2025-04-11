from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.reservation import ReservationCreate, ReservationOut
from src.services.reservation_service import get_all_reservations, create_reservation, delete_reservation
from src.database import get_async_session


router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=list[ReservationOut])
async def read_reservations(db: AsyncSession = Depends(get_async_session)):
    return await get_all_reservations(db)


@router.post("/", response_model=ReservationOut, status_code=201)
async def add_reservation(reservation: ReservationCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        reservation = await create_reservation(db, reservation)
        return reservation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reservation_id}", response_model=ReservationOut)
async def remove_reservation(reservation_id: int, db: AsyncSession = Depends(get_async_session)):
    reservation = await delete_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
