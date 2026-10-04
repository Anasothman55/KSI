from core.models import UnitEnum
import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints

ItemsSku = Annotated[
  str, StringConstraints(max_length=64)
]
ItemsBrand = Annotated[ #? nullable
  str, StringConstraints(max_length=128, min_length=2, pattern=r"^[A-Za-z0-9_]+$", strip_whitespace=True)
]
ItemsTitle = Annotated[
  str, StringConstraints(max_length=128, min_length=3, strip_whitespace=True)
]
ItemsFormalName = Annotated[ #? nullable
  str, StringConstraints(max_length=128, min_length=3, pattern=r"^[A-Za-z0-9_]+$", strip_whitespace=True)
]



class ItemsBaseSchema(BaseModel):
  title: ItemsTitle
  base_unit: UnitEnum


class ItemsSchema(ItemsBaseSchema):
  uid: uuid.UUID
  sku: ItemsSku
  brand: ItemsBrand | None = None
  formal_name: ItemsFormalName
  description: str | None = None
  extra: dict | None = None
  created_at: datetime
  updated_at: datetime


class ItemsCreateSchema(ItemsBaseSchema):
  brand: ItemsBrand | None = None
  formal_name: ItemsFormalName
  description: str | None = None
  extra: dict | None = None


class ItemsUpdateSchema(BaseModel):
  title: ItemsTitle | None = None
  base_unit: UnitEnum | None = None
  brand: ItemsBrand | None = None
  formal_name: ItemsFormalName | None = None
  description: str | None = None
  extra: dict | None = None




#! response





