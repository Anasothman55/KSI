import uuid
from typing import Annotated

from pydantic import StringConstraints, BaseModel, Field

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
  manager: UsersBaseSchema | None = None

class UsersReadSchema(UsersSchema):
  manager: UsersBaseSchema

# class UsersReadMultiSchema(BaseModel):
#   name: NAME
#   phone_numbers: PHONE_NUMBER_TYPE
#
# manager_uid
# manager
# employees













