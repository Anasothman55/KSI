from typing import Annotated, Any
import uuid

from fastapi import status, APIRouter, Depends, Query, HTTPException
from fastapi.responses import  JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from core.models import ItemConditionEnum
from routes.items.inventory.service import create, read, update, delete, read_multi
from routes.items.inventory.schema import (
  InventoryUpdateSchema,
  InventoryCreateSchema,
  InventorySchema
)

api = APIRouter(
  prefix="/inventory",
  tags=["inventory"],
)

@api.get('/enum')
async def get_enum():
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      'condition': {r.name: r.value for r in ItemConditionEnum},
    }
  )


@api.post("/", response_model=InventorySchema)
async def create_inventory(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: InventoryCreateSchema,
):
  return await create(db=db, body=body)


@api.get("/", deprecated=True)
async def read_inventory(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: Annotated[str | None, Query(max_length=128)] = None,
    page: Annotated[int | None, Query(ge=1)] = 1,
    items_per_page: Annotated[int | None, Query(ge=1, le=100)] = 100
):
  #return await read_multi(db=db, name=name, page=page or 1, items_per_page=items_per_page or 10)
  raise HTTPException(
    status_code=status.HTTP_410_GONE,
    detail="This endpoint has been deprecated and is no longer available.",
  )

@api.get("/{uid}", deprecated=True)
async def read_inventory(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
):
  #return await read(db=db, uid=uid)
  raise HTTPException(
    status_code=status.HTTP_410_GONE,
    detail="This endpoint has been deprecated and is no longer available.",
  )


@api.patch("/{uid}", status_code=status.HTTP_200_OK, response_model=InventorySchema)
async def update_inventory(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: Any,
):
  return await update(db=db, uid=uid, body=body)


@api.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await delete(db=db, uid=uid)









