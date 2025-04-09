from sqlalchemy import Column, Integer, String
from src.database import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
