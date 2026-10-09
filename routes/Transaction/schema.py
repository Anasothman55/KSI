import uuid
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal, LiteralString

from pydantic import BaseModel, StringConstraints, Field, ConfigDict, model_validator, TypeAdapter, ValidationError
from pydantic_core import PydanticCustomError, InitErrorDetails

from core.config import PROJECT_DATETIME
from core.models import TransactionTypeEnum, TransactionOperationEnum

TransactionTitle= Annotated[str, StringConstraints(min_length=1, max_length=64, strip_whitespace=True)]
TransactionsDateTime = Annotated[datetime, Field(le=PROJECT_DATETIME.get_datetime())]
TransactionsSupplier = Annotated[str, StringConstraints(min_length=1, max_length=64, strip_whitespace=True)]
TransactionsTotalAmount = Annotated[Decimal, Field(ge=0)]
TransactionsCurrency= Literal['USD', 'IQD', 'EUR']
TransactionsRecip=Annotated[str, StringConstraints(min_length=1, max_length=64, strip_whitespace=True)]

class TransactionsBaseSchema(BaseModel):
  title: TransactionTitle
  t_date: TransactionsDateTime
  t_type: TransactionTypeEnum
  t_operations: TransactionOperationEnum
  is_active: bool

class TransactionsEssentialSchema(BaseModel):
  uid: uuid.UUID
  created_at: datetime
  updated_at: datetime

class TransactionsExtraFieldSchema(BaseModel):
  note: str | None = None

class TransactionsNoneSchema(BaseModel):
  purchaser_uid: uuid.UUID | None = None
  supplier: TransactionsSupplier | None = None
  total_amount: TransactionsTotalAmount | None = None
  currency: TransactionsCurrency | None = None
  recip: TransactionsRecip | None = None

  @model_validator(mode="after")
  def validate_purchase(self):
    if self.purchaser_uid is not None:
      missing = []
      if self.supplier is None: missing.append("supplier")
      if self.total_amount is None:missing.append("total_amount")
      if self.currency is None:missing.append("currency")
      if self.recip is None: missing.append("recip")

      if missing:

        errors = [
          InitErrorDetails(
            type= PydanticCustomError(
              "missing",
              "Field '{field}' is required when purchaser_uid is provided",
              {"field": field},
            ),
            loc=("body", field),
            input=None,

          ) for field in missing
        ]

        raise ValidationError.from_exception_data(
          self.__class__.__name__,
          errors,
        )

    return self

  model_config = ConfigDict(
      extra="forbid",
      str_strip_whitespace=True,
  )

class TransactionsSchema( TransactionsBaseSchema,TransactionsEssentialSchema, TransactionsNoneSchema, TransactionsExtraFieldSchema):
  pass


class TransactionsCreateSchema(TransactionsExtraFieldSchema, TransactionsNoneSchema):
  title: TransactionTitle
  t_date: TransactionsDateTime
  t_type: TransactionTypeEnum

class TransactionsUpdateSchema(TransactionsNoneSchema):
  pass

class TransactionsReadSchema:
  pass

class TransactionsReadMultiSchema:
  pass

#! response

class TransactionsResponseSchema(TransactionsSchema):
  pass

class TransactionsCreateResponseSchema(TransactionsResponseSchema):
  pass

class TransactionsUpdateResponseSchema:
  pass

class TransactionsReadResponseSchema:
  pass

class TransactionsReadMultiResponseSchema:
  pass


# query


class TransactionReadMultiQuery(BaseModel):
  search: str | None = Field(None)







