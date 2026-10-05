import uuid
from typing import Annotated, Any

from fastapi import HTTPException, status
from fastcrud import FastCRUD, paginated_response, compute_offset, JoinConfig
from fastcrud.core.query import joins
from rich import print
from sqlalchemy import func, select, String, cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased

from core.models import ItemsModel, ItemsVariantModel
from routes.varinats.schema import ItemsVariantReadCodeSchema
from routes.items.schema import (
  ItemsCreateSchema,
  ItemsSchema,
  ItemsUpdateSchema,
  ItemsReadMultiSchema,
  ItemsCreateSchemaToSelect
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

    max_number: int = (
      await db.execute(select(func.max(ItemsModel.sku_number)).where(ItemsModel.variant_uid == body.variant_uid))
    ).scalar_one()


    data= ItemsCreateSchemaToSelect(**body.model_dump(), sku_number= (max_number or 0) + 1)

    item = (await items_crud.create(
      db=db,
      object=data,
      schema_to_select=ItemsSchema,
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
  page: int  = 1,
  items_per_page: int = 10,
):
  filters = []
  if name is not None:
    filters.append(ItemsModel.title.ilike(f"%{name}%"))

  variant = aliased(ItemsVariantModel)

  offset = (page - 1) * items_per_page

  # Total count
  count_stmt = (
      select(func.count())
      .select_from(ItemsModel)
      .where(*filters)
  )

  total_count = await db.scalar(count_stmt)

  sku = func.concat(
    ItemsVariantModel.sku_code,
    "-",
    func.lpad(cast(ItemsModel.sku_number, String), 6, "0"),
  ).label("sku")

  res = (await db.execute(
    select(ItemsModel,sku )
    .join( ItemsVariantModel,ItemsModel.variant_uid == ItemsVariantModel.uid,)
    .where(*filters)
    .offset(offset)
    .limit(items_per_page)
  )).all()

  rows = [
    {**ItemsSchema.model_validate(item, from_attributes=True).model_dump(), 'sku': sku}
    for item, sku in res
  ]

  return {
    "data": rows,
    "total_count": total_count,
    "page": page,
    "items_per_page": items_per_page,
    "has_more": offset < total_count
  }

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