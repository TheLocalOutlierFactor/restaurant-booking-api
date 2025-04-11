from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.table import TableOut, TableCreate
from src.services.table_service import get_all_tables, create_table, delete_table
from src.database import get_async_session


router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=list[TableOut])
async def read_tables(db: AsyncSession = Depends(get_async_session)):
    return await get_all_tables(db)


@router.post("/", response_model=TableOut)
async def add_table(table: TableCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_table(db, table)


@router.delete("/{table_id}", response_model=TableOut)
async def remove_table(table_id: int, db: AsyncSession = Depends(get_async_session)):
    table = await delete_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table
