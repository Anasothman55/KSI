import uvicorn
from fastapi import FastAPI, Request
from fastapi.exception_handlers import (
  http_exception_handler,
  request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exceptions.exceptions import register_exception_handlers, AppException
from core.lifespan import lifespan, tag_metadata
from core.success_response import success_response, PaginationSuccessResponse
from routes.categories.api import api as categories_api
from routes.items.api import items_api
from routes.users.api import api as users_api
from routes.varinats.api import api as variant_api
from routes.Transaction.api import transaction_api

app = FastAPI(
  title='Kolak Inv API',
  version='0.1.0',

  contact={
    "name": 'Anas Othman Ezzat',
    "email": 'anasothman581@gmail.com',
  },

  lifespan=lifespan,
  openapi_tags= tag_metadata
)

register_exception_handlers(app)

app.include_router(users_api, prefix="/api")
app.include_router(categories_api, prefix="/api")
app.include_router(variant_api, prefix="/api")
app.include_router(items_api, prefix="/api")
app.include_router(transaction_api, prefix="/api")


@app.get("/")
async def root(
    error_example: bool = False
):
  if not error_example:

   return success_response(
     status_code=200,
     content= {
       "message": "Welcome to Kolak Inv API",
     }
   )

  raise AppException(
    error_dict={
      "status_code": 500,
      "headers": {"WWW-Authenticate": "Bearer"},
      "error": {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "An internal server error occurred",
        "detail": []
      }
    }
  )


if __name__ == '__main__':

  uvicorn.run(
    app='main:app',
    port=8000,
    reload=True,
    host='localhost',
  )
