import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ItemsModel, PackagingModel
from routes.items.packagin.schema import PackagingCreateSchema, PackagingUpdateSchema
from routes.shared.func import integrity_error_raise


async def create(
    db: AsyncSession,
    body: PackagingCreateSchema
):
  try:

    if (await db.execute(select(ItemsModel).where(ItemsModel.uid == body.item_uid))).scalar_one_or_none() is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    level = PackagingModel(**body.model_dump())

    db.add(level)
    await db.commit()
    await db.refresh(level)
    return level

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
)-> PackagingModel | None:
  return (await db.execute(
    select(PackagingModel).where(PackagingModel.uid == uid)
  )).scalar_one_or_none()



async def update(
    db: AsyncSession,
    uid: uuid.UUID,
    body: PackagingUpdateSchema
):
  try:

    if level := (await read(db, uid)):

      for f,v in body.model_dump().items():
        setattr(level, f.name, v)

      await db.commit()
      await db.refresh(level)
      return level

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Packaging not found")

  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def delete(
    db: AsyncSession,
    uid: uuid.UUID,
):
  if level := (await read(db, uid)):
    await db.delete(level)
    await db.commit()

  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Packaging not found")







