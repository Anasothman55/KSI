import uuid
from typing import Annotated, TYPE_CHECKING

from pydantic import BaseModel, StringConstraints, ConfigDict, AfterValidator

VariantName = Annotated[
  str, StringConstraints(max_length=128, min_length=2, strip_whitespace=True)
]

VariantSkuCode = Annotated[
  str, StringConstraints(max_length=5, min_length=1, strip_whitespace=True), AfterValidator(lambda v: v.upper())
]


class ItemsVariantBaseSchema(BaseModel):
  name: VariantName
  sku_code: VariantSkuCode

class ItemsVariantSchema(ItemsVariantBaseSchema):
  uid: uuid.UUID

class ItemsVariantCreateSchema(ItemsVariantBaseSchema):
  pass

class ItemsVariantUpdateSchema(BaseModel):
  name: VariantName | None = None
  sku_code: VariantSkuCode

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra="forbid",
  )


class ItemsVariantReadSchema(ItemsVariantSchema):
  pass

class ItemsVariantReadMultiSchema(ItemsVariantSchema):
  pass

class ItemsVariantReadCodeSchema(BaseModel):
  sku_code: VariantSkuCode


#! response

class ItemsVariantResponseSchema(ItemsVariantSchema):
  pass

class ItemsVariantCreateResponseSchema(ItemsVariantResponseSchema):
  pass

class ItemsVariantUpdateResponseSchema(ItemsVariantResponseSchema):
  pass

class ItemsVariantReadResponseSchema(ItemsVariantResponseSchema):
  pass

class ItemsVariantReadMultiResponseSchema(BaseModel):
  data: list[ItemsVariantReadMultiSchema]
  total_count: int
  has_more: bool
  page: int
  items_per_page: int
