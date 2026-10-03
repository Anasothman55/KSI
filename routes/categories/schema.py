import uuid
from typing import Annotated

from pydantic import BaseModel, StringConstraints



CATEGORIES_NAME = Annotated[str, StringConstraints(max_length=128, min_length=3, pattern=r"^[A-Za-z0-9_]+$", strip_whitespace=True)]

class BaseCategoriesSchema(BaseModel):
  name: CATEGORIES_NAME

class CategoriesSchema(BaseCategoriesSchema):
  uid: uuid.UUID
  description:  str | None = None

class CategoriesCreateSchema(BaseCategoriesSchema):
  description: str | None = None

class CategoriesUpdateSchema(BaseModel):
  name: CATEGORIES_NAME | None = None
  description: str | None = None

class CategoriesRaedMultiSchema(CategoriesSchema):
  pass

# Response

class CategoriesCreateResponseSchema(CategoriesCreateSchema):
  uid: uuid.UUID

class CategoriesUpdateResponseSchema(CategoriesUpdateSchema):
  uid: uuid.UUID

class CategoriesReadMultiResponseShema(BaseModel):
  data: list[CategoriesRaedMultiSchema]
  total_count: int



