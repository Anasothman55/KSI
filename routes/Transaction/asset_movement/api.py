import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from routes.Transaction.asset_movement.service import create, read, read_multi, update, delete

api = APIRouter(
  prefix="/movement",
  tags=["Asset Movement"],
)


@api.post("/")
async def create_movement(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: Any
):
  return await create(db, body)

@api.get("/")
async def read_multi_movement(
    db: Annotated[AsyncSession, Depends(get_db)],
    search: Annotated[str | None, Query(max_length=128)] = None,
    page: Annotated[int | None, Query(ge=1)] = 1,
    items_per_page: Annotated[int | None, Query(ge=1, le=100)] = 100
):
  return await read_multi(db, search, page or 1, items_per_page or 100)


@api.get("/{uid}")
async def read_movement(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await read(db, uid)

@api.patch("/{uid}")
async def update_movement(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: Any
):
  return await update(db, uid, body)

@api.delete("/{uid}")
async def delete_movement(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await delete(db, uid)