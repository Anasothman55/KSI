import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from routes.items.packagin.schema import (
  PackagingCreateResponseSchema,
  PackagingCreateSchema,
  PackagingUpdateResponseSchema,
  PackagingUpdateSchema,
)
from routes.items.packagin.service import create, delete, read, read_multi, update

api = APIRouter(
  prefix="/packaging",
  tags=["Packaging"],
)



@api.post("/", response_model=PackagingCreateResponseSchema)
async def create_packaging(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: PackagingCreateSchema,
):
  return await create(db=db, body=body)


@api.get("/", deprecated=True)
async def read_packaging(
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
async def read_packaging(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
):
  #return await read(db=db, uid=uid)
  raise HTTPException(
    status_code=status.HTTP_410_GONE,
    detail="This endpoint has been deprecated and is no longer available.",
  )


@api.patch("/{uid}", status_code=status.HTTP_200_OK, response_model=PackagingUpdateResponseSchema)
async def update_packaging(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: PackagingUpdateSchema,
):
  return await update(db=db, uid=uid, body=body)


@api.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_packaging(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await delete(db=db, uid=uid)









