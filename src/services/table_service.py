from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.models.table import Table
from src.schemas.table import TableCreate
from src.utils.exceptions import UniqueConstraintError


async def get_all_tables(db: AsyncSession):
    result = await db.execute(select(Table))
    return result.scalars().all()


async def create_table(db: AsyncSession, table: TableCreate):
    db_table = Table(**table.model_dump())
    db.add(db_table)
    try:
        await db.commit()
    except IntegrityError as e:
        if e.orig.sqlstate == "23505":  # Error 23505 is UniqueConstraintViolation (from IntegrityError subclass)
            await db.rollback()
            raise UniqueConstraintError
        await db.rollback()
        raise e  # Raise original IntegrityError if it is unrelated to UniqueConstraintViolation
    await db.refresh(db_table)
    return db_table


async def delete_table(db: AsyncSession, table_id: int):
    result = await db.execute(select(Table).where(Table.id == table_id))
    db_table = result.scalars().first()
    if db_table:
        await db.delete(db_table)
        await db.commit()
    return db_table
