import uuid
from enum import StrEnum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, Text, ARRAY, Enum, ForeignKey

from core.db import Base
from core.types import PHONE_NUMBER_TYPE


class UsersStatus(StrEnum):
  active = "active"
  inactive = "inactive"
  banned = "banned"
  terminated = "terminated"

class UsersRole(StrEnum):
  employee = "employee"
  client = "client"
  contractor = "contractor"
  supplier = "supplier"
  contractor_employee = "contractor_employee"


class UsersModel(Base):

  __tablename__ = "users"

  uid: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default= uuid.uuid7)
  name: Mapped[str] = mapped_column(String(128), unique=True, )
  phone_numbers: Mapped[PHONE_NUMBER_TYPE] = mapped_column(String, nullable=False)
  status: Mapped[UsersStatus] = mapped_column(
    Enum( UsersStatus, name="users_status_enum", create_type=True,), nullable=False, default=UsersStatus.active
  )
  role: Mapped[UsersRole] = mapped_column(
    Enum( UsersRole, name="users_role_enum", create_type=True,), nullable=False, default=UsersRole.employee
  )
  description: Mapped[str | None] = mapped_column(Text, default=None)

  manager_uid: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.uid", ondelete='SET NULL'), nullable=True)
  manager: Mapped[Optional["UsersModel"]] = relationship(
    "UsersModel",
    remote_side=[uid],
    back_populates="employees",
    lazy='select',
  )

  employees: Mapped[list["UsersModel"] | None] = relationship(
    "UsersModel",
    back_populates="manager",
    lazy='select',
  )





