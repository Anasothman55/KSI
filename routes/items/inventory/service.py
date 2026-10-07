import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ItemsInventoryModel, ItemsModel
from routes.shared.func import integrity_error_raise
from routes.items.inventory.schema import (
  InventoryCreateSchema,
  InventoryUpdateSchema,
)

async def create(
    db: AsyncSession,
    body: InventoryCreateSchema
):
  try:

    if (await db.execute(select(ItemsModel).where(ItemsModel.uid == body.item_uid))).scalar_one_or_none() is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    inv = ItemsInventoryModel(**body.model_dump())

    db.add(inv)
    await db.commit()
    await db.refresh(inv)
    return inv

  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def read_multi(
    db: AsyncSession,
    name: str | None = None,
    page: int = 1,
    items_per_page: int = 10,
):
  pass

async def read(
    db: AsyncSession,
    uid: uuid.UUID,
)-> ItemsInventoryModel | None:
  return (await db.execute(
    select(ItemsInventoryModel).where(ItemsInventoryModel.uid == uid)
  )).scalar_one_or_none()



async def update(
    db: AsyncSession,
    uid: uuid.UUID,
    body: InventoryUpdateSchema
):
  try:

    if inv := (await read(db, uid)):

      for f,v in body.model_dump().items():
        setattr(inv, f.name, v)

      await db.commit()
      await db.refresh(inv)
      return inv

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def delete(
    db: AsyncSession,
    uid: uuid.UUID,
):
  if inv := (await read(db, uid)):
    await db.delete(inv)
    await db.commit()

  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")







