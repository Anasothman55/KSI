import uuid
from typing import Annotated

from pydantic import StringConstraints, BaseModel, Field, ConfigDict

from core.models import UsersStatus, UsersRole
from core.types import PHONE_NUMBER_TYPE

NAME = Annotated[
  str, StringConstraints(min_length=3, max_length=128, strip_whitespace=True), Field(examples=['Anas Othman'])
]
DESCRIPTION = Annotated[str | None, StringConstraints(strip_whitespace=True)]


class UsersBaseSchema(BaseModel):
  uid: uuid.UUID
  name: NAME

class UsersSchema(UsersBaseSchema):
  phone_numbers: PHONE_NUMBER_TYPE
  status: UsersStatus
  role: UsersRole
  manager_uid: uuid.UUID | None
  description: DESCRIPTION

  model_config = ConfigDict(
    from_attributes=True
  )

class UsersCreateSchema(BaseModel):
  name: NAME
  phone_numbers: PHONE_NUMBER_TYPE
  status: UsersStatus
  role: UsersRole
  manager_uid: uuid.UUID | None
  description: DESCRIPTION

class UsersUpdateSchema(BaseModel):
  name: NAME | None
  phone_numbers: PHONE_NUMBER_TYPE | None
  status: UsersStatus | None
  role: UsersRole | None
  manager_uid: uuid.UUID | None
  description: DESCRIPTION | None


class UsersCreateResponseSchema(UsersSchema):
  pass

class UsersReadManagerSchema(UsersBaseSchema):
  role: UsersRole
  model_config = ConfigDict(
    from_attributes=True
  )

class UsersReadSchema(UsersSchema):
  manager: UsersReadManagerSchema | None = None
  employees: list[UsersSchema]

  model_config = ConfigDict(
    from_attributes=True
  )

class UsersReadMultiSchema(UsersSchema):
  pass

class UsersReadMultiManagerSchema(BaseModel):
  name: NAME

class UsersReadMultiResDataSchema(UsersReadMultiSchema):
  manager_name: NAME | None

class UsersReadMultiResSchema(BaseModel):
  data: list[UsersReadMultiResDataSchema]
  total_count: int

# class UsersReadMultiSchema(BaseModel):
#   name: NAME
#   phone_numbers: PHONE_NUMBER_TYPE
#
# manager_uid
# manager
# employees













