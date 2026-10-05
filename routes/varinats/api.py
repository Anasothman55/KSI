import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from routes.varinats.service import create, delete, read, read_multi, update
from routes.varinats.schema import (
  ItemsVariantCreateSchema,
  ItemsVariantCreateResponseSchema,
  ItemsVariantReadResponseSchema,
  ItemsVariantReadMultiResponseSchema,
  ItemsVariantUpdateResponseSchema
)

api = APIRouter(
  prefix="/variants",
  tags=["Variants"],
)



@api.post("/", response_model=ItemsVariantCreateResponseSchema)
async def create_variant(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: ItemsVariantCreateSchema,
):
  return await create(db=db, body=body)


@api.get("/", response_model=ItemsVariantReadMultiResponseSchema)
async def read_variants(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: Annotated[str | None, Query(max_length=128)] = None,
    page: Annotated[int | None, Query(ge=1)] = 1,
    items_per_page: Annotated[int | None, Query(ge=1, le=100)] = 100
):
  return await read_multi(db=db, name=name, page=page, items_per_page=items_per_page)


@api.get("/{uid}", response_model=ItemsVariantReadResponseSchema)
async def read_variant(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
):
  return await read(db=db, uid=uid)


@api.patch("/{uid}", response_model=ItemsVariantUpdateResponseSchema, status_code=status.HTTP_200_OK)
async def update_variant(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: Any,
):
  return await update(db=db, uid=uid, body=body)


@api.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await delete(db=db, uid=uid)
