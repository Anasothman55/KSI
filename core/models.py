from core.config import PROJECT_DATETIME
from datetime import datetime, date , time
import uuid
from enum import StrEnum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, Text, ARRAY, Enum, ForeignKey, TIMESTAMP, Table, Column
from sqlalchemy.dialects.postgresql import JSONB

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




item_categories = Table(
  "item_categories",
  Base.metadata,
  Column("item_uid", ForeignKey("items.uid", ondelete="CASCADE"), primary_key=True),
  Column("category_uid", ForeignKey("categories.uid", ondelete="CASCADE"), primary_key=True),
)


class CategoriesModel(Base):
  __tablename__ = "categories"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid7)
  name: Mapped[str] = mapped_column(String(128), unique=True)
  description: Mapped[str | None] = mapped_column(Text, default=None)
  items: Mapped[list["ItemsModel"]] = relationship(
    secondary=item_categories,
    back_populates="categories",
  )


class ItemsModel(Base):
  __tablename__ = "items"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid7)
  sku: Mapped[str] = mapped_column(String(64), unique=True) 
  brand: Mapped[str | None] = mapped_column(String(128), default=None)
  title: Mapped[str] = mapped_column(String(128))
  formal_name: Mapped[str | None] = mapped_column(String(128), default=None)
  base_unit: Mapped[str] = mapped_column(String(32))
  description: Mapped[str | None] = mapped_column(Text, default=None)
  extra: Mapped[dict | None] = mapped_column(JSONB, default=None)
  created_at: Mapped[datetime] = mapped_column(
      TIMESTAMP(timezone=False), default=PROJECT_DATETIME.get_datetime
  )
  updated_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=False),
    default=PROJECT_DATETIME.get_datetime,
    onupdate=PROJECT_DATETIME.get_datetime,
  )
  categories: Mapped[list[CategoriesModel]] = relationship(
    secondary=item_categories,
    back_populates="items",
  )