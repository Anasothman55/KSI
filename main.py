import uvicorn
from fastapi import FastAPI, Request
from fastapi.exception_handlers import (
  http_exception_handler,
  request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.lifespan import lifespan
from routes.categories.api import api as categories_api
from routes.items.api import items_api
from routes.users.api import api as users_api
from routes.varinats.api import api as variant_api

app = FastAPI(
  title='Kolak Inv API',
  version='0.1.0',

  contact={
    "name": 'Anas Othman Ezzat',
    "email": 'anasothman581@gmail.com',
  },

  lifespan=lifespan,
)


app.include_router(users_api, prefix="/api")
app.include_router(categories_api, prefix="/api")
app.include_router(variant_api, prefix="/api")
app.include_router(items_api, prefix="/api")

@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
):
  return await http_exception_handler(request, exception)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
  return await request_validation_exception_handler(request, exception)


if __name__ == '__main__':

  uvicorn.run(
    app='main:app',
    port=8000,
    reload=True,
    host='localhost',
  )
