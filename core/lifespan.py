from contextlib import asynccontextmanager
from fastapi import FastAPI
from rich import print

from core.db import db_init, close_db

tag_metadata= [
  {"name": "Users Crud"},
  {"name": "Categories"},
  {"name": "Variants"},
  {
    "name": "Items",
    "description": "after we add transaction route go to add selection load for items get so we can get the packaging level"
  },
  {"name": "Inventory"},
  {"name": "Packaging"},
  {"name": "Transactions"},
  {"name": "Asset Movement"}
]
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



