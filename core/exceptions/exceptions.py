from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from core.exceptions.error_schema import ErrorDetailSchema, ExceptionSchema, ErrorSchema, ErrorContent, ErrorDict


async def general_http_exception_handler(
    request: Request,
    exception: HTTPException,
):
  return



class AppException(Exception):

  def __init__(
      self,
      error_dict: ErrorDict
  ):
    self.error_dict = error_dict

    super().__init__(self.error_dict['error']['message'])



async def app_exception_handler(
    request: Request,
    exc: AppException,
):
  return JSONResponse(
    status_code=exc.error_dict["status_code"],
    content={
      "success": False,
      "error": exc.error_dict["error"]
    },
    headers=exc.error_dict["headers"],
  )


def register_exception_handlers(app: FastAPI):

  app.add_exception_handler(
    AppException,
    app_exception_handler  # type: ignore[arg-type]
  )

  app.add_exception_handler(
    HTTPException,
    general_http_exception_handler  # type: ignore[arg-type]
  )





