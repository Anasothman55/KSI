from core.models import UnitEnum
from fastapi.responses import JSONResponse
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from routes.items.service import create, delete, read, read_multi, update

from routes.items.schema import (
  ItemsCreateSchema,
  ItemsUpdateSchema,
)

api = APIRouter(
  prefix="/items",
  tags=["Items"],
)

@api.get('/enum')
async def get_enum():
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      'unit': {r.name: r.value for r in UnitEnum},
    }
  )


@api.post("/", response_model=Any)
async def create_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    body: ItemsCreateSchema,
):
  return await create(db=db, body=body)


@api.get("/", response_model=Any)
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


@api.patch("/{uid}", response_model=Any, status_code=status.HTTP_200_OK)
async def update_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID,
    body: Any,
):
  return await update(db=db, uid=uid, body=body)


@api.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    uid: uuid.UUID
):
  return await delete(db=db, uid=uid)
