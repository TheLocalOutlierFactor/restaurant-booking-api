from pydantic import BaseModel, Field


class TableBase(BaseModel):
    name: str = Field(min_length=1, max_length=128, examples=["Столик 1"])
    seats: int = Field(ge=1, default=1, examples=[4])
    location: str = Field(min_length=1, max_length=128, examples=["Терраса"])

class TableCreate(TableBase):
    pass

class TableOut(TableBase):
    id: int

    class Config:
        from_attributes = True
