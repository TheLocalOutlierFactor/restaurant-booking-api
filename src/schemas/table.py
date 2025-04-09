from pydantic import BaseModel, Field


class TableBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    seats: int = Field(ge=1, default=1)
    location: str = Field(min_length=1, max_length=128)

class TableCreate(TableBase):
    pass

class TableOut(TableBase):
    id: int

    class Config:
        from_attributes = True
