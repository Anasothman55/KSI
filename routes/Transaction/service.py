import uuid
from typing import Any
from rich import print

from fastapi import HTTPException, status
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import TransactionModel, TransactionOperationEnum, UsersModel
from core.models import TransactionTypeEnum as TTE
from routes.Transaction.schema import TransactionsCreateSchema, TransactionReadMultiQuery
from routes.shared.filters import apply_filter


async def create(
    db: AsyncSession,
    body: TransactionsCreateSchema
):

  operation = TransactionOperationEnum.OUT
  if body.t_type in [TTE.PURCHASE, TTE.RETURN]: operation = TransactionOperationEnum.IN
  if body.t_type in [TTE.ADJUSTMENT, TTE.WRITE_OFF, TTE.ASSEMBLY, TTE.DISASSEMBLY]: operation = TransactionOperationEnum.INTERNAL

  if body.purchaser_uid is not None:
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
):

  print(filters_query)
  print(filters_query.model_dump())
  print(filters_query.model_dump(exclude_none=True, exclude={"page", "items_per_page", "search"}))

  where = []
  if filters_query.search:
    where.append(
      or_(
        TransactionModel.title.ilike(f"%{filters_query.search}%"),
        TransactionModel.note.ilike(f"%{filters_query.search}%"),
      )
    )
  
  print(select(TransactionModel, ).where(*where))

  page = filters_query.page or 1
  items_per_page = filters_query.items_per_page

  offset = (page - 1) * items_per_page
  # Total count
  total_count = (await db.scalar(
    select(func.count())
    .select_from(TransactionModel)
    .where(*where)
  ))

  print(    select(TransactionModel, )
    .where(*where)
    .offset(offset)
    .limit(items_per_page))

  res = (await db.execute(
    select(TransactionModel, )
    .where(*where)
    .offset(offset)
    .limit(items_per_page)
  )).scalars().all()


  return {
    "data": res,
    "total_count": total_count,
    "page": page,
    "items_per_page": items_per_page,
    "has_more": offset < total_count
  }


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

