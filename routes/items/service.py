import uuid
from typing import Annotated, Any

from fastapi import HTTPException, status
from fastcrud import FastCRUD
from rich import print
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ItemsModel, ItemsVariantModel
from routes.items.schema import (
  ItemsCreateSchema,
  ItemsUpdateSchema,
)
from routes.shared.func import integrity_error_raise

items_crud = FastCRUD(ItemsModel)

async def create(
  db: AsyncSession, 
  body: ItemsCreateSchema
):
  try:

    variant: ItemsVariantModel | None = (await db.execute(select(ItemsVariantModel).where(ItemsVariantModel.uid == body.variant_uid))).scalar_one_or_none()
    if variant is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The variant dose not exist")

    max_number: int = (await db.execute(select(func.max(ItemsModel.sku_number)).where(ItemsModel.variant_uid == body.variant_uid))).scalar_one()

    body.sku_number = (max_number or 0) + 1

    item = (await items_crud.create(
      db=db,
      object=body,
      schema_to_select=ItemsCreateSchema,
      commit=True,
    ))

    return item
    
  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def read(
  db: AsyncSession, 
  uid: uuid.UUID
):
  pass

async def read_multi(
  db: AsyncSession,
  name: str | None = None, 
  offset: int = 0, 
  limit: int = 100
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