import re

from fastapi import HTTPException, status
from psycopg import errors
from sqlalchemy.exc import IntegrityError

# def integrity_error_raise(e: IntegrityError):
#   orig = str(e.orig)
#   parts = orig.split("\n", 1)
#   error = parts[0]
#   extra = parts[1] if len(parts) > 1 else ""
#   field, value = re.findall(r"\((.*?)\)", extra)
#   raise HTTPException(
#     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#     detail={
#       "error": error,
#       "message": extra,
#       "field": field,
#       "value": value,
#     },
#   ) from e


#! recheck this code 
def integrity_error_raise(e: IntegrityError):
    orig = e.orig

    # UNIQUE
    if isinstance(orig, errors.UniqueViolation):
        detail = orig.detail or ""

        match = re.search(
            r"Key \((?P<field>.*?)\)=\((?P<value>.*?)\) already exists",
            detail,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "unique_violation",
                "message": "A record with this value already exists.",
                "field": match.group("field") if match else None,
                "value": match.group("value") if match else None,
                "constraint": orig.constraint_name,
            },
        ) from e

    # FOREIGN KEY / RESTRICT
    if isinstance(orig, errors.ForeignKeyViolation):
        detail = orig.detail or ""

        # DELETE/UPDATE RESTRICT
        match = re.search(
            r"Key \((?P<field>.*?)\)=\((?P<value>.*?)\) "
            r"is still referenced from table \"(?P<table>.*?)\"",
            detail,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "foreign_key_violation",
                "message": (
                    "This record cannot be deleted or changed because "
                    "it is still referenced by another record."
                ),
                "field": match.group("field") if match else None,
                "value": match.group("value") if match else None,
                "referenced_table": match.group("table") if match else None,
                "constraint": orig.constraint_name,
            },
        ) from e

    # NOT NULL
    if isinstance(orig, errors.NotNullViolation):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "not_null_violation",
                "message": f"Field '{orig.column_name}' cannot be null.",
                "field": orig.column_name,
                "value": None,
                "constraint": orig.constraint_name,
            },
        ) from e

    # Unknown integrity error
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "integrity_error",
            "message": str(orig),
        },
    ) from e





