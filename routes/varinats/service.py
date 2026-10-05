import uuid

from fastcrud import FastCRUD, compute_offset, paginated_response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ItemsVariantModel
from routes.shared.func import integrity_error_raise
from routes.varinats.schema import (
  ItemsVariantCreateSchema,
  ItemsVariantReadMultiSchema,
  ItemsVariantReadSchema,
  ItemsVariantUpdateSchema,
)

variant_crud = FastCRUD(ItemsVariantModel)



async def create(
  db: AsyncSession, 
  body: ItemsVariantCreateSchema
):
  try:
    
    variant = ItemsVariantModel(**body.model_dump())

    db.add(variant)
    await db.commit()
    await db.refresh(variant)

    return variant
    
  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def read(
  db: AsyncSession, 
  uid: uuid.UUID
):
  
  return await variant_crud.get(
    db=db,
    uid=uid,
    schema_to_select=ItemsVariantReadSchema,
  )

async def read_multi(
  db: AsyncSession,
  name: str | None = None, 
  page: int = 1,
  items_per_page: int = 10,
):
  filters = {}
  if name is not None:
    filters['name__ilike'] = f"%{name}%"
  
  data=  await variant_crud.get_multi(
    db=db,
    schema_to_select=ItemsVariantReadMultiSchema,
    offset=compute_offset(page, items_per_page),
    limit=items_per_page,
    **filters
  )


  return paginated_response(
    crud_data=data,
    page=page,
    items_per_page=items_per_page,
  )


async def update(
  db: AsyncSession, 
  uid: uuid.UUID, 
  body: ItemsVariantUpdateSchema
):
  try:

    variant = await variant_crud.update(
      db=db,
      uid=uid,
      object=body.model_dump(exclude_none=True),
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
    await variant_crud.delete(db=db, uid=uid, commit=True)
  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)