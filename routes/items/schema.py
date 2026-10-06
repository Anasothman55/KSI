from core.models import UnitEnum
import uuid
from datetime import datetime
from typing import Annotated, TYPE_CHECKING

from pydantic import BaseModel, StringConstraints, Field, ConfigDict, computed_field

from routes.varinats.schema import ItemsVariantResponseSchema

ItemsBrand = Annotated[ #? nullable
  str, StringConstraints(max_length=128, min_length=2, pattern=r"^[A-Za-z0-9_]+$", strip_whitespace=True)
]
ItemsTitle = Annotated[
  str, StringConstraints(max_length=128, min_length=3, strip_whitespace=True)
]
ItemsFormalName = Annotated[ #? nullable
  str, StringConstraints(max_length=128, min_length=3, strip_whitespace=True)
]



class ItemsBaseSchema(BaseModel):
  title: ItemsTitle
  base_unit: UnitEnum

class ItemsExtraSchema(BaseModel):
  sku_number: int
  formal_name: ItemsFormalName
  variant_uid: uuid.UUID

class ItemsEssentialSchema(BaseModel):
  uid: uuid.UUID
  created_at: datetime
  updated_at: datetime

class ItemsNullableSchema(BaseModel):
  brand: ItemsBrand | None = None
  description: str | None = None
  extra: dict | None = None

class ItemsSchema(ItemsEssentialSchema,ItemsExtraSchema,ItemsBaseSchema, ItemsNullableSchema):
  pass

class ItemsCreateSchema(ItemsBaseSchema, ItemsNullableSchema):
  formal_name: ItemsFormalName
  variant_uid: uuid.UUID
  categories_uid: list[uuid.UUID] = []

  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True
  )



class ItemsUpdateSchema(ItemsNullableSchema):
  title: ItemsTitle | None = None
  base_unit: UnitEnum | None = None
  formal_name: ItemsFormalName | None = None
  categories_uid: list[uuid.UUID] = []

  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True
  )

class ItemsReadMultiSchema(ItemsSchema):
  sku: str

class ItemsReadSchema(ItemsSchema):
  variant: ItemsVariantResponseSchema

#! response

class ItemsCreateResponseSchema(ItemsSchema):
  pass

class ItemsReadResponseSchema(ItemsSchema):
  sku: str
  variant: ItemsVariantResponseSchema

class ItemsReadMultiResponseSchema(BaseModel):
  data: list[ItemsReadMultiSchema]
  total_count: int
  has_more: bool
  page: int
  items_per_page: int
