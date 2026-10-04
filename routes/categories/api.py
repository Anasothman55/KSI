import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from routes.categories.schema import (
  CategoriesCreateResponseSchema,
  CategoriesCreateSchema,
  CategoriesReadMultiResponseShema,
  CategoriesUpdateResponseSchema,
  CategoriesUpdateSchema,
)
from routes.categories.service import create, delete, read, read_multi, update

api = APIRouter(
  prefix="/categories",
  tags=["Categories"],
)


@api.post("/", response_model=CategoriesCreateResponseSchema)
async def create_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: CategoriesCreateSchema,
):
  return await create(db=db, body=body)


@api.get("/", response_model=CategoriesReadMultiResponseShema)
async def read_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: Annotated[str | None, Query(max_length=128)] = None
):
  return await read_multi(db=db, name=name)


@api.get("/{uid}")
async def read_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
):
  return await read(db=db, uid=uid)


@api.patch("/{uid}", response_model=CategoriesUpdateResponseSchema, status_code=status.HTTP_200_OK)
async def update_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: CategoriesUpdateSchema,
):
  return await update(db=db, uid=uid, body=body)


@api.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await delete(db=db, uid=uid)

