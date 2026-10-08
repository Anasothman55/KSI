import uuid
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

PackagingName = Annotated[
  str, StringConstraints(min_length=1, max_length=128, strip_whitespace=True)
]

PackagingUnit = Annotated[
  str, StringConstraints(min_length=1, max_length=32, strip_whitespace=True)
]


class PackagingBaseSchema(BaseModel):
  unit: PackagingUnit
  change_rate: Decimal = Field(gt=0.0)

class PackagingEssentialsSchema(BaseModel):
  uid: uuid.UUID

class PackagingSchema(PackagingBaseSchema, PackagingEssentialsSchema):
  name: PackagingName
  item_uid: uuid.UUID

class PackagingCreateSchema(PackagingBaseSchema):
  name: PackagingName
  item_uid: uuid.UUID

class PackagingUpdateSchema(BaseModel):
  unit: PackagingUnit | None = None
  change_rate: Decimal | None = Field(None, gt=0.0)
  name: PackagingName | None = None

# response


class PackagingCreateResponseSchema(PackagingSchema):
  pass

class PackagingUpdateResponseSchema(PackagingSchema):
  pass











