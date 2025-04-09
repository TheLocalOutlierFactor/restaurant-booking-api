from pydantic import BaseModel, Field
from datetime import datetime

from src.schemas.table import TableBase


class ReservationBase(BaseModel):
    customer_name: str = Field(min_length=1, max_length=128)
    table_id: int = TableBase
    reservation_time: datetime
    duration_minutes: int = Field(ge=1)

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    id: int

    class Config:
        from_attributes = True
