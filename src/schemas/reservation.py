from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas.table import TableBase


class ReservationBase(BaseModel):
    customer_name: str = Field(min_length=1, max_length=128, examples=["Геннадий Степанов"])
    table_id: int = TableBase
    reservation_time: datetime = Field(examples=["2025-04-09T18:00:00"])
    duration_minutes: int = Field(ge=1, examples=[20])


class ReservationCreate(ReservationBase):
    pass


class ReservationOut(ReservationBase):
    id: int

    class Config:
        from_attributes = True
