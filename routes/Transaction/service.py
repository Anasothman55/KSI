import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


async def create(
    db: AsyncSession,
    body: Any
):
  pass

async def read_multi(
    db: AsyncSession,
    search: str | None = None,
    page: int = 1,
    items_per_page: int = 100
):
  pass

async def read(
    db: AsyncSession,
    uid: uuid.UUID
):
  pass

async def update(
    db: AsyncSession,
    uid: uuid.UUID,
    body: Any
):
  pass

async def delete(
    db: AsyncSession,
    uid: uuid.UUID
):
  pass

