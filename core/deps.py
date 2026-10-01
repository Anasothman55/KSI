from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
  async with SessionLocal() as session:
    try:
      yield session
    except  Exception as e:
      await session.rollback()
      raise