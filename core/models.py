import uuid
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import (
  TIMESTAMP,
  UUID,
  Column,
  Enum,
  ForeignKey,
  Numeric,
  String,
  Table,
  Text,
  UniqueConstraint,
  Integer,
  DateTime
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.config import PROJECT_DATETIME
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
  manager: Mapped[UsersModel | None] = relationship(
    "UsersModel",
    remote_side=[uid],
    back_populates="employees",
    lazy='select',
  )

  employees: Mapped[list[UsersModel] | None] = relationship(
    "UsersModel",
    back_populates="manager",
    lazy='select',
  )

  transactions: Mapped[list["TransactionModel"]] = relationship(
    "TransactionModel",
    back_populates="purchaser",
  )




item_categories = Table(
  "item_categories",
  Base.metadata,
  Column("item_uid", ForeignKey("items.uid", ondelete="CASCADE"), primary_key=True),
  Column("category_uid", ForeignKey("categories.uid", ondelete="CASCADE"), primary_key=True),
)


class CategoriesModel(Base):
  __tablename__ = "categories"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid7)
  name: Mapped[str] = mapped_column(String(128), unique=True)
  description: Mapped[str | None] = mapped_column(Text, default=None)

  items: Mapped[list[ItemsModel]] = relationship(
    secondary=item_categories,
    back_populates="categories",
  )


class UnitEnum(StrEnum):
  """Units of measure for inventory items."""

  # Count
  PIECE = "pc"
  DOZEN = "dz"
  PACK = "pk"
  BOX = "box"
  CARTON = "ctn"
  PALLET = "plt"
  # Weight
  MILLIGRAM = "mg"
  GRAM = "g"
  KILOGRAM = "kg"
  OUNCE = "oz"
  POUND = "lb"
  TON = "t"
  # Volume
  MILLILITER = "ml"
  LITER = "l"
  FLUID_OUNCE = "fl oz"
  GALLON = "gal"
  # Length
  MILLIMETER = "mm"
  CENTIMETER = "cm"
  METER = "m"
  INCH = "in"
  FOOT = "ft"



class ItemsModel(Base):
  __tablename__ = "items"
  
  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid7)
  sku_number: Mapped[int] = mapped_column(Integer,nullable=False,)
  brand: Mapped[str | None] = mapped_column(String(128), default=None)
  title: Mapped[str] = mapped_column(String(128))
  formal_name: Mapped[str] = mapped_column(String(128), )
  base_unit: Mapped[UnitEnum] = mapped_column(
    Enum(UnitEnum, name="unit_enum", create_type=True, values_callable=lambda e: [m.value for m in e]), nullable=False, default=UnitEnum.PIECE.value
  )
  description: Mapped[str | None] = mapped_column(Text, default=None)
  extra: Mapped[dict | None] = mapped_column(JSONB, default=None)
  variant_uid: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("items_variant.uid", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=True)
  created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=False), default=PROJECT_DATETIME.get_datetime
  )
  updated_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=False),default=PROJECT_DATETIME.get_datetime,onupdate=PROJECT_DATETIME.get_datetime,
  )

  categories: Mapped[list[CategoriesModel]] = relationship(
    secondary=item_categories,
    back_populates="items",
  )

  inventory: Mapped[list[ItemsInventoryModel]] = relationship(
    "ItemsInventoryModel",
    back_populates="item",
  )

  packaging: Mapped[list[PackagingModel]] = relationship(
    "PackagingModel",
    back_populates="item",
  )

  variant: Mapped[ItemsVariantModel | None] = relationship(
    "ItemsVariantModel",
    back_populates="items",
  )

  __table_args__ = (
    UniqueConstraint(
      "variant_uid",
      "sku_number",
      name="uq_items_variant_sku_number",
    ),
  )

class ItemsVariantModel(Base):
  __tablename__ = "items_variant"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid7)
  name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
  sku_code: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)

  items: Mapped[list[ItemsModel]] = relationship(
    "ItemsModel",
    back_populates="variant",
  )


class ItemConditionEnum(StrEnum):
  new = 'new'
  used = 'used'
  damaged = 'damaged'
  broken = 'broken'
  lost = 'lost'

class ItemsInventoryModel(Base):

  __tablename__ = "items_inventory"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid7)
  condition: Mapped[ItemConditionEnum] = mapped_column(
    Enum(ItemConditionEnum, name="item_condition_enum", create_type=True), nullable=False, default=ItemConditionEnum.new
  )
  owner: Mapped[str] = mapped_column(String(64), nullable=False)

  item_uid: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.uid", ondelete="CASCADE"), nullable=False)
  item: Mapped[ItemsModel] = relationship("ItemsModel", back_populates="inventory")

  asset_movements: Mapped[list["AssetMovementModel"]] = relationship(
    "AssetMovementModel",
    back_populates="item_inventory",
    cascade="all, delete-orphan",
  )

  created_at: Mapped[datetime] = mapped_column(
      TIMESTAMP(timezone=False), default=PROJECT_DATETIME.get_datetime
  )
  updated_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=False),default=PROJECT_DATETIME.get_datetime,onupdate=PROJECT_DATETIME.get_datetime,
  )

  __table_args__ = (
    UniqueConstraint("item_uid", "owner", 'condition'),
  )


class PackagingModel(Base):
  __tablename__ = "packaging"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid7)
  name: Mapped[str] = mapped_column(String(128), nullable=False)
  unit: Mapped[str] = mapped_column(String(32), nullable=False)
  change_rate: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

  item_uid: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.uid", ondelete="CASCADE"), nullable=False)

  item: Mapped[ItemsModel] = relationship("ItemsModel", back_populates="packaging")

  __table_args__ = (
    UniqueConstraint("item_uid", "name"),
  )


class TransactionTypeEnum(StrEnum):
  MAINTENANCE = "maintenance"
  PURCHASE = "purchase"
  SEND_BACK = "send_back"
  BARROW = "barrow"
  RETURN = "return"
  USAGE = "usage"
  ADJUSTMENT = "adjustment"
  WRITE_OFF = "write_off"
  SALE = "sale"
  ASSEMBLY = "assembly"
  DISASSEMBLY = "disassembly"

class TransactionOperationEnum(StrEnum):
  IN = "in"
  OUT = "out"
  INTERNAL = "internal"


class TransactionModel(Base):
  __tablename__ = "transaction"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)

  title: Mapped[str] = mapped_column(String(64), nullable=False)
  t_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
  t_type: Mapped[TransactionTypeEnum] = mapped_column(
    Enum(TransactionTypeEnum, name="transaction_type_enum", create_type=True, values_callable=lambda e: [m.value for m in e]), nullable=False, default=TransactionTypeEnum.USAGE.value
  )
  t_operations: Mapped[TransactionOperationEnum] = mapped_column(
    Enum(TransactionOperationEnum, name="transaction_operation_enum", create_type=True, values_callable=lambda e: [m.value for m in e]), nullable=False, default=TransactionOperationEnum.OUT.value
  )
  note: Mapped[str | None] = mapped_column(Text, nullable=True, )

  # purchase
  purchaser_uid: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.uid", ondelete="SET NULL"), nullable=True)
  purchaser: Mapped[UsersModel | None] = relationship(
    "UsersModel",
    back_populates="transactions",
  )
  asset_movements: Mapped[list["AssetMovementModel"]] = relationship(
    "AssetMovementModel",
    back_populates="transaction",
    cascade="all, delete-orphan",
  )
  supplier: Mapped[str | None] = mapped_column(String(64), nullable=True)
  total_amount: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
  currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
  recip: Mapped[str | None] = mapped_column(String(64), nullable=True)

  created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), default=PROJECT_DATETIME.get_datetime)
  updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False),default=PROJECT_DATETIME.get_datetime,onupdate=PROJECT_DATETIME.get_datetime,)


  __table_args__ = (
    UniqueConstraint("recip", "supplier"),
  )


class AssetMovementModel(Base):
  __tablename__ = "asset_movement"

  uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)

  transaction_uid: Mapped[uuid.UUID] = mapped_column(ForeignKey("transaction.uid", ondelete="CASCADE"), nullable=False)
  transaction: Mapped[TransactionModel] = relationship(
    "TransactionModel",
    back_populates="asset_movements",
  )
  item_inventory_uid: Mapped[uuid.UUID] = mapped_column(ForeignKey("items_inventory.uid", ondelete="CASCADE"), nullable=False)
  item_inventory: Mapped[ItemsInventoryModel] = relationship(
    "ItemsInventoryModel",
    back_populates="asset_movements",
  )
  quantity: Mapped[Decimal] = mapped_column(Numeric, nullable=False,)

  unite_price: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True,)

  note: Mapped[str | None] = mapped_column(Text, nullable=True,)

  created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), default=PROJECT_DATETIME.get_datetime)
  updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False),default=PROJECT_DATETIME.get_datetime,onupdate=PROJECT_DATETIME.get_datetime,)

