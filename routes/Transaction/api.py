import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from routes.Transaction.service import create, read, read_multi, update, delete
from routes.Transaction.asset_movement.api import api as movement_api
from routes.Transaction.schema import (
  TransactionsCreateSchema,
  TransactionsCreateResponseSchema, TransactionReadMultiQuery
)

transaction_api = APIRouter(prefix="/transaction")

api = APIRouter(
  tags=["Transactions"],
)

transaction_api.include_router(movement_api)
transaction_api.include_router(api)


@api.post("/", response_model=TransactionsCreateResponseSchema)
async def create_transaction(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: TransactionsCreateSchema
):
  return await create(db, body)

@api.get("/")
async def read_multi_transaction(
    db: Annotated[AsyncSession, Depends(get_db)],
    filters_query: Annotated[TransactionReadMultiQuery, Query()],
):
  return await read_multi(db, filters_query)


@api.get("/{uid}")
async def read_transaction(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await read(db, uid)

@api.patch("/{uid}")
async def update_transaction(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: Any
):
  return await update(db, uid, body)

@api.delete("/{uid}")
async def delete_transaction(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await delete(db, uid)