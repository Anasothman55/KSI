import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints

from core.models import ItemConditionEnum


InventoryOwner = Annotated[
  str, StringConstraints(min_length=2, max_length=64, strip_whitespace=True)
]


class InventoryBaseSchema(BaseModel):
  condition: ItemConditionEnum
  owner: InventoryOwner

class InventoryEssentialsSchema(BaseModel):
  uid: uuid.UUID
  created_at: datetime
  updated_at: datetime

class InventorySchema(InventoryBaseSchema, InventoryEssentialsSchema):
  item_uid: uuid.UUID

class InventoryCreateSchema(InventoryBaseSchema):
  item_uid: uuid.UUID

class InventoryUpdateSchema(BaseModel):
  condition: ItemConditionEnum | None = None
  owner: InventoryOwner | None = None

# response


class InventoryCreateResponseSchema(InventorySchema):
  pass

class InventoryUpdateResponseSchema(InventorySchema):
  pass











