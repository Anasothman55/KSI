from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from routes.users.schema import UsersCreateSchema, UsersCreateResponseSchema
from routes.users.service import create


api = APIRouter(
  prefix="/users",
  tags=["Users Crud"]
)

@api.post('/', response_model=UsersCreateResponseSchema)
async def create_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: UsersCreateSchema
):
  return await create(db, body)

@api.get('/')
async def multi_users():
  pass

@api.get('/{uid}')
async def users():
  pass

@api.put('/{uid}')
async def update_user():
  pass

@api.delete('/{uid}')
async def delete_user():
  pass

















