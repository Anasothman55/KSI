import uuid

from fastapi import HTTPException, status
from fastcrud import FastCRUD
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import CategoriesModel
from routes.categories.schema import (
  CategoriesCreateResponseSchema,
  CategoriesCreateSchema,
  CategoriesRaedMultiSchema,
  CategoriesUpdateSchema,
)
from routes.shared.func import integrity_error_raise

category_crud = FastCRUD(CategoriesModel)

async def create(
    db: AsyncSession,
    body: CategoriesCreateSchema,
):
  try:
    return await category_crud.create(
      db=db,
      object=body,
      schema_to_select=CategoriesCreateResponseSchema,
      commit=True,
    )
  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def read_multi(
    db: AsyncSession,
    name: str | None = None,
):
  filters = {}
  if name is not None:
    filters['name__ilike'] = f"%{name}%"

  return await category_crud.get_multi(
    db=db,
    schema_to_select=CategoriesRaedMultiSchema,

    return_total_count=True,
    **filters
  )


async def read(
    db: AsyncSession,
    uid: uuid.UUID,
):
  # manager = aliased(UsersModel)
  # employees = aliased(UsersModel)

  stmt = (
    select(CategoriesModel)
    .where(CategoriesModel.uid == uid)
    # .options(
    #   selectinload(
    #     UsersModel.manager.of_type(manager)
    #   ).load_only(
    #     manager.uid, # type: ignore
    #     manager.name, # type: ignore
    #     manager.role, # type: ignore
    #   ),
    #   selectinload(
    #     UsersModel.employees.of_type(employees)
    #   )
    # )
  )

  result = await db.execute(stmt)
  category: CategoriesModel | None = result.scalar_one_or_none()

  if category:
    return category

  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Category not found",
  )

async def update(
    db: AsyncSession,
    uid: uuid.UUID,
    body: CategoriesUpdateSchema,
):
  try:
    res =  await category_crud.update(
      db=db,
      object=body.model_dump(exclude_none=True),
      schema_to_select=CategoriesCreateResponseSchema,
      commit=True,

      uid=uid,
    )

    if res is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category with uid {uid} not found",
      )

    return res

  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def delete(
    db: AsyncSession,
    uid: uuid.UUID,
):
  await category_crud.db_delete(
    db=db,
    uid=uid
  )