from typing import TypedDict

from pydantic import BaseModel



class ErrorDetail(TypedDict):
  field: str | None
  code: str
  message: str

class ErrorContent(TypedDict):
  code: str
  message: str
  detail: list[ErrorDetail] | None

class ErrorDict(TypedDict):
  """
    {
      "status_code": 500,
      "headers": {"WWW-Authenticate": "Bearer"},
      "error": {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "An internal server error occurred",
        "detail": []
      }
    }
  """

  error: ErrorContent
  status_code: int
  headers: dict[str, str] | None

class ErrorDetailSchema(BaseModel):
  field: str | None = None
  code: str
  message: str


class ErrorSchema(BaseModel):
  code: str
  message: str
  detail: list[ErrorDetailSchema] | None = None

class ExceptionSchema(BaseModel):
  error: ErrorSchema



