import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from core.models import UnitEnum
from routes.items.schema import (
  ItemsCreateResponseSchema,
  ItemsCreateSchema,
  ItemsReadMultiResponseSchema,
  ItemsReadResponseSchema,
  ItemsUpdateSchema,
  ItemsUpdateResponseSchema
)
from routes.items.service import create, delete, read, read_multi, update
from routes.items.inventory.api import api as inventory_api
from routes.items.packagin.api import api as packaging_api

items_api = APIRouter(prefix="/items")

api = APIRouter(
  tags=["Items"],
)

items_api.include_router(inventory_api)
items_api.include_router(packaging_api)
items_api.include_router(api)

@api.get('/enum')
async def get_enum():
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      'unit': {r.name: r.value for r in UnitEnum},
    }
  )


@api.post("/", response_model=ItemsCreateResponseSchema)
async def create_item(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: ItemsCreateSchema,
):
  return await create(db=db, body=body)


@api.get("/", response_model=ItemsReadMultiResponseSchema)
async def read_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: Annotated[str | None, Query(max_length=128)] = None,
    page: Annotated[int | None, Query(ge=1)] = 1,
    items_per_page: Annotated[int | None, Query(ge=1, le=100)] = 100
):
  return await read_multi(db=db, name=name, page=page or 1, items_per_page=items_per_page or 10)


@api.get("/{uid}", response_model=ItemsReadResponseSchema)
async def read_item(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
):
  return await read(db=db, uid=uid)


@api.patch("/{uid}", response_model=ItemsUpdateResponseSchema, status_code=status.HTTP_200_OK)
async def update_item(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: ItemsUpdateSchema,
):
  return await update(db=db, uid=uid, body=body)


@api.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT, deprecated=True)
async def delete_item(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  #return await delete(db=db, uid=uid)
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      "message": "Item delete don't work",
    }
  )
