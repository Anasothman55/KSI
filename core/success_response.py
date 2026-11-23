from typing import Any

from pydantic import BaseModel
from fastapi.responses import JSONResponse


class PaginationSuccessResponse(BaseModel):
  data: list[Any]
  total_count: int
  page: int
  items_per_page: int
  has_more: bool

def success_response(
    content: dict | list | PaginationSuccessResponse | str,
    status_code: int = 200,
):

  return JSONResponse(
    status_code=status_code,
    content={
      "success": True,
      "content": content
    }
  )





