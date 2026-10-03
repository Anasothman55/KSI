from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

import re


def integrity_error_raise(e: IntegrityError):
  orig = str(e.orig)
  parts = orig.split("\n", 1)
  error = parts[0]
  extra = parts[1] if len(parts) > 1 else ""
  field, value = re.findall(r"\((.*?)\)", extra)
  raise HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail={
      "error": error,
      "message": extra,
      "field": field,
      "value": value,
    },
  ) from e








