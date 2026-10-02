import uuid
from typing import Annotated, Any
from rich import print

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from core.deps import get_db
from core.models import UsersRole, UsersStatus
from routes.users.schema import (
  UsersCreateSchema,
  UsersCreateResponseSchema,
  UsersReadMultiResSchema,
  UsersReadSchema,
)
from routes.users.service import create, get_multi, get, delete


api = APIRouter(
  prefix="/users",
  tags=["Users Crud"]
)

@api.get('/enum')
async def get_enum():
  print({
      'role': UsersRole,
      'status': UsersStatus,
    })
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      'role': [r.value for r in UsersRole],
      'status': [s.name for s in UsersStatus],
    }
  )

@api.post('/', response_model=UsersCreateResponseSchema)
async def create_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: UsersCreateSchema
) -> Any :
  return await create(db, body)

@api.get('/', response_model=UsersReadMultiResSchema)
async def multi_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: Annotated[str | None, Query(min_length=1, max_length=128)] = None
)-> Any:
  return await get_multi(db, name)

@api.get('/{uid}', response_model=UsersReadSchema)
async def users(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
) -> Any:
  return await get(db, uid)

@api.put('/{uid}')
async def update_user() -> Any:
  pass

@api.delete('/{uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  await delete(db, uid)















