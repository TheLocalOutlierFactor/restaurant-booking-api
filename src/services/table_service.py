from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.models.table import Table
from src.schemas.table import TableCreate
from src.utils.error_messages import TABLE_EXISTS


async def get_all_tables(db: AsyncSession):
    result = await db.execute(select(Table))
    return result.scalars().all()


async def create_table(db: AsyncSession, table: TableCreate):
    db_table = Table(**table.model_dump())
    db.add(db_table)
    try:
        await db.commit()
    except IntegrityError as e:
        if e.orig.sqlstate == "23505":  # Ошибка 23505 это Unique Constraint Violation
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail=TABLE_EXISTS
            )
        await db.rollback()
        raise  # Ошибка все равно бросается, если она не связана с дубликатом имени
    await db.refresh(db_table)
    return db_table


async def delete_table(db: AsyncSession, table_id: int):
    result = await db.execute(select(Table).where(Table.id == table_id))
    db_table = result.scalars().first()
    if db_table:
        await db.delete(db_table)
        await db.commit()
    return db_table
