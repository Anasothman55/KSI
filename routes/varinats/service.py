from core.models import ItemsVariantModel
import uuid
from typing import Annotated, Any

from fastcrud import FastCRUD
from rich import print
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ItemsModel

from routes.shared.func import integrity_error_raise

from routes.varinats.schema import (
  ItemsVariantCreateSchema,
  ItemsVariantUpdateSchema,
  ItemsVariantReadSchema,
  ItemsVariantReadMultiSchema
)

items_crud = FastCRUD(ItemsVariantModel)



async def create(
  db: AsyncSession, 
  body: ItemsVariantCreateSchema
):
  try:

    variant = await items_crud.create(
      db=db,
      object=body,
      schema_to_select=ItemsVariantCreateSchema,
      commit=True,
    )

    return variant
    
  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def read(
  db: AsyncSession, 
  uid: uuid.UUID
):
  
  return await items_crud.get(
    db=db,
    uid=uid,
    schema_to_select=ItemsVariantReadSchema,
  )

async def read_multi(
  db: AsyncSession,
  name: str | None = None, 
  offset: int = 0, 
  limit: int = 100
):
  filters = {}
  if name is not None:
    filters['name__ilike'] = f"%{name}%"
  
  return await items_crud.get_multi(
    db=db,
    schema_to_select=ItemsVariantReadMultiSchema,
    offset=offset,
    limit=limit,
    **filters
  )


async def update(
  db: AsyncSession, 
  uid: uuid.UUID, 
  body: ItemsVariantUpdateSchema
):
  try:

    variant = await items_crud.update(
      db=db,
      uid=uid,
      object=body,
      schema_to_select=ItemsVariantUpdateSchema,
      commit=True,
    )

    return variant
    
  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def delete(
  db: AsyncSession,
  uid: uuid.UUID
):
  try:
    await items_crud.delete(db=db, uid=uid, commit=True)
  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)