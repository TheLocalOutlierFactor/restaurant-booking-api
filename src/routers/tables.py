from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.table import TableOut, TableCreate
from src.services.table_service import get_all_tables, create_table, delete_table
from src.database import get_async_session
from src.utils import exceptions


router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=list[TableOut])
async def read_tables(db: AsyncSession = Depends(get_async_session)):
    return await get_all_tables(db)


@router.post("/", response_model=TableOut, status_code=201)
async def add_table(table: TableCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        table = await create_table(db, table)
        return table
    except exceptions.UniqueConstraintError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{table_id}", response_model=TableOut)
async def remove_table(table_id: int, db: AsyncSession = Depends(get_async_session)):
    table = await delete_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail=exceptions.TABLE_NOT_FOUND)
    return table
