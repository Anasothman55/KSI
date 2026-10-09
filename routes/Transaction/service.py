import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import TransactionModel, TransactionOperationEnum, UsersModel
from core.models import TransactionTypeEnum as TTE
from routes.Transaction.schema import TransactionsCreateSchema, TransactionReadMultiQuery


async def create(
    db: AsyncSession,
    body: TransactionsCreateSchema
):

  operation = TransactionOperationEnum.OUT
  if body.t_type in [TTE.PURCHASE, TTE.RETURN]: operation = TransactionOperationEnum.IN
  if body.t_type in [TTE.ADJUSTMENT, TTE.WRITE_OFF, TTE.ASSEMBLY, TTE.DISASSEMBLY]: operation = TransactionOperationEnum.INTERNAL

  purchaser_user = (await db.execute(select(UsersModel).where(UsersModel.uid == body.purchaser_uid))).scalar_one_or_none()
  if not purchaser_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Purchaser user does not exist")

  new_transaction = TransactionModel(
    **body.model_dump(exclude_none=True),
    t_operations= operation
  )

  db.add(new_transaction)
  await db.commit()
  await db.refresh(new_transaction)

  return new_transaction


async def read_multi(
    db: AsyncSession,
    filters_query: TransactionReadMultiQuery,
    page: int = 1,
    items_per_page: int = 100
):
  pass

async def read(
    db: AsyncSession,
    uid: uuid.UUID
):
  pass

async def update(
    db: AsyncSession,
    uid: uuid.UUID,
    body: Any
):
  pass

async def delete(
    db: AsyncSession,
    uid: uuid.UUID
):
  pass

