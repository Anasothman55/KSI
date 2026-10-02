from fastapi import HTTPException, status
from fastcrud import FastCRUD, JoinConfig
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from functools import wraps
import re
import uuid
from rich import print

from core.models import UsersModel
from routes.users.schema import (
  UsersCreateSchema,
  UsersCreateResponseSchema,
  UsersReadMultiManagerSchema,
  UsersReadMultiSchema,
  UsersReadSchema,
  UsersReadManagerSchema, UsersUpdateSchema
)


user_crud = FastCRUD(UsersModel)


def integrity(func):
  @wraps(func)
  async def wrapper(*args, **kwargs):
    db: AsyncSession = args[0]

    try:
      return await func(*args, **kwargs)
    except ValueError as e:
      await db.rollback()
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e),
      ) from e
    except IntegrityError as e:
      await db.rollback()
      orig = str(e.orig)
      parts = orig.split("\n", 1)
      error = parts[0]
      extra = parts[1] if len(parts) > 1 else ""
      field, value = re.findall(r"\((.*?)\)", extra)
      raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
          "error": error,
          "message": extra,
          "field": field,
          "value": value,
        },
      ) from e
  return wrapper


@integrity
async def create(
    db: AsyncSession,
    body: UsersCreateSchema,
):

  new_user = await user_crud.create(
    db=db,
    object=body,
    schema_to_select=UsersCreateResponseSchema,
    return_as_model=True,
    commit=False,
  )

  if body.manager_uid is not None:
    manager = await user_crud.get(
      db=db,
      uid=body.manager_uid,
    )
    if manager is None:
      raise ValueError(
        f"Manager with uid {body.manager_uid} not found"
      )

  await db.commit()

  return new_user



async def get_multi(
    db: AsyncSession,
    name: str | None = None,
):
  manager = aliased(UsersModel)

  filters = {}

  if name is not None:
    filters['name__ilike'] = f"%{name}%"
  
  return await user_crud.get_multi_joined(
    db=db,
    schema_to_select=UsersReadMultiSchema,

    join_model=UsersModel,
    alias=manager,
    join_on=UsersModel.manager_uid == manager.uid,
    join_prefix="manager_",
    join_schema_to_select=UsersReadMultiManagerSchema,
    join_type="left",

    **filters,
  )

async def get(
    db: AsyncSession,
    uid: uuid.UUID,
) -> UsersModel:
  manager = aliased(UsersModel)
  employees = aliased(UsersModel)

  stmt = (
    select(UsersModel)
    .where(UsersModel.uid == uid)
    .options(
      selectinload(
        UsersModel.manager.of_type(manager)
      ).load_only(
        manager.uid, # type: ignore
        manager.name, # type: ignore
        manager.role, # type: ignore
      ),
      selectinload(
        UsersModel.employees.of_type(employees)
      )
    )
  )

  result = await db.execute(stmt)
  user: UsersModel | None = result.scalar_one_or_none()

  if user:
    return user

  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
  )

@integrity
async def update(
    db: AsyncSession,
    uid: uuid.UUID,
    body: UsersUpdateSchema,
):
  # 1. Lock and load the user being updated
  user = (await db.execute(select(UsersModel.uid).where(UsersModel.uid == uid).with_for_update())).one_or_none()

  if user is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  if body.manager_uid is not None:

    if uid == body.manager_uid:
      raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="User cannot be their own manager",)

    current_uid = body.manager_uid
    visited: set[uuid.UUID] = set()

    while current_uid is not None:
      if current_uid in visited:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Existing management cycle detected in hierarchy",)

      visited.add(current_uid)

      row = (
        await db.execute(
          select(UsersModel.uid, UsersModel.manager_uid)
          .where(UsersModel.uid == current_uid)
          .with_for_update()
        )
      ).one_or_none()

      if row is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manager not found",)

      row_uid, parent_uid = row

      if row_uid == uid: raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Invalid manager: this would create a management cycle",)

      current_uid = parent_uid

  # 3. Apply the update (exclude_unset lets manager_uid be explicitly set to null)
  updated_user = await user_crud.update(
      db=db,
      object=body.model_dump(exclude_unset=True),
      schema_to_select=UsersCreateResponseSchema,
      return_as_model=True,
      commit=False,
      uid=uid,
  )

  await db.commit()
  return updated_user

async def delete(
    db: AsyncSession,
    uid: uuid.UUID,
):
  await user_crud.db_delete(
    db=db,
    uid=uid
  )

