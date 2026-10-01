from fastcrud import FastCRUD
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UsersModel
from routes.users.schema import (
  UsersCreateSchema,
  UsersCreateResponseSchema
)


user_crud = FastCRUD(UsersModel)

async def create(
    db: AsyncSession,
    body: UsersCreateSchema,
):
  try:
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
        object_id=body.manager_uid,
      )
      if manager is None:
        raise ValueError(
          f"Manager with uid {body.manager_uid} not found"
        )

    await db.commit()

    return new_user

  except ValueError:
    await db.rollback()
    raise
  except IntegrityError as e:
    await db.rollback()
    raise ValueError(["User with this name already exists", str(e), e.detail, e.__dict__])









