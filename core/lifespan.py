from contextlib import asynccontextmanager
from fastapi import FastAPI
from rich import print

from core.db import db_init, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
  try:

    await db_init()
    print("Database initialized")

  except Exception as e:
    print(f"Error during application startup: {e}")
    raise

  yield

  try:
    await close_db()
    print("Database closed")

  except Exception as e:
    print(f"Error during application shutdown: {e}")



