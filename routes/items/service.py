import uuid
from typing import Annotated, Any

from fastcrud import FastCRUD
from rich import print
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ItemsModel
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

    sku_g = body.formal_name.split("_")
    
    print(sku_g)
    # item = await items_crud.create(
    #   db=db,
    #   object=body,
    #   schema_to_select=ItemsCreateSchema,
    #   commit=True,
    # )

    return 'item'
    
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