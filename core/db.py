
from typing import Any
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
  pass


engine: AsyncEngine = create_async_engine(
  url=settings.db_url,
  echo= False,

  pool_size=10,
  max_overflow=20,
  pool_timeout=30,
  pool_recycle=3600,
  pool_pre_ping=True,
)


SessionLocal = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False,
)


async def db_init() -> Any:
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  async with SessionLocal() as session:
    res = await session.scalar(text('SELECT 1'))
    print(f"Database connection successful: {res}")

async def close_db() -> Any:
  await engine.dispose()




















