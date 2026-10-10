from typing import TypeVar, Literal, Generic, Any

from fastapi import Query
from pydantic import BaseModel, model_validator, ConfigDict, Field
from sqlalchemy import ColumnElement

FilterOp = Literal["eq", "neq", "gt", "gte", "lt", "lte", "between",'in', 'nin','il','nil','isn', 'isnn']
FilterOpList: list[FilterOp] = ["eq", "neq", "gt", "gte", "lt", "lte", "between",'in', 'nin','il','nil','isn', 'isnn']

def create_field[F](name: str, op: list[FilterOp] = FilterOpList )-> dict:
  fields = {}
  for o in op:
    if o == "between":
      fields[f'{name}_between_start'] = (F | None, Field(None))
      fields[f'{name}_between_end'] = (F | None, Field(None))
      continue

    if o in ['in', 'nin']:
      fields[f'{name}_in'] = (list[F] | None, Field(None))
      fields[f'{name}_not_in'] = (list[F] | None, Field(None))
      continue

    if o in ['isn', 'isnn']:
      fields[f'{name}_is_null'] = (bool | None, Field(default=False))
      fields[f'{name}_is_not_null'] = (bool | None, Field(default=False))
      continue

    fields[f'{name}_{o}'] = (F | None, Field(None))

  return fields


def create_where(
    column: ColumnElement,
    filter_query: dict[str, Any],
) -> list:
    where = []

    cn = column.key
    column_filter = {k: v for k, v in filter_query.items() if k.startswith(f"{cn}_")}

    b_start = column_filter.get(f"{cn}_between_start")
    b_end = column_filter.get(f"{cn}_between_end")

    if b_start is not None or b_end is not None:
      if b_start is None or b_end is None:
        raise ValueError(f"'{cn}_between' requires both start and end")
      if b_start > b_end:
        raise ValueError(f"'{cn}_between_start' must be less than or equal to '{cn}_between_end'")
      where.append(column.between(b_start, b_end))

    if (v := column_filter.get(f"{cn}_eq")) is not None: where.append(column == v)
    if (v := column_filter.get(f"{cn}_neq")) is not None: where.append(column != v)
    if (v := column_filter.get(f"{cn}_gt")) is not None: where.append(column > v)
    if (v := column_filter.get(f"{cn}_gte")) is not None: where.append(column >= v)
    if (v := column_filter.get(f"{cn}_lt")) is not None: where.append(column < v)
    if (v := column_filter.get(f"{cn}_lte")) is not None: where.append(column <= v)
    if (v := column_filter.get(f"{cn}_il")) is not None: where.append(column.ilike(f"%{v}%"))
    if (v := column_filter.get(f"{cn}_nil")) is not None: where.append(column.not_ilike(f"%{v}%"))
    if column_filter.get(f"{cn}_is_null") is True:where.append(column.is_(None))
    if column_filter.get(f"{cn}_is_not_null") is True:where.append(column.is_not(None))
    if (v := column_filter.get(f"{cn}_in")) is not None:
      if len(v) == 0: raise ValueError(f"'{cn}_in' cannot be empty")
      where.append(column.in_(v))

    if (v := column_filter.get(f"{cn}_not_in")) is not None:
      if len(v) == 0: raise ValueError(f"'{cn}_not_in' cannot be empty")
      where.append(column.not_in(v))


    return where




class Filter[T](BaseModel):
  op: FilterOp
  value: T | None = None
  in_value: list[T] | None = []
  start: T | None = None
  end: T | None = None

  @model_validator(mode="after")
  def validate_filter(self):
    if self.op == "between":
      if self.start is None or self.end is None:
        raise ValueError("'between' requires start and end")

      if self.start > self.end:
        raise ValueError("start must be less than or equal to end")

    if self.op in ['in', 'nin']:
      if self.in_value is None:
        raise ValueError("in and not in requires list value")

    if self.op in ['isn', 'isnn']:
      if self.in_value is not None:
        raise ValueError("is null and is not null don't requires value")

    elif self.value is None:
      raise ValueError(f"'{self.op}' requires value")

    return self

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra="forbid"
  )

def apply_filter(
    column: ColumnElement,
    filters: Filter,
) -> ColumnElement:

  match filters.op:
    case "eq":
      return column == filters.value

    case "neq":
      return column != filters.value

    case "gt":
      return column > filters.value

    case "gte":
      return column >= filters.value

    case "lt":
      return column < filters.value

    case "lte":
      return column <= filters.value

    case "il":
      return column.ilike(f"%{filters.value}%")

    case "nil":
      return column.notilike(f"%{filters.value}%")

    case "isn":
      return column.is_(None)

    case "isnn":
      return column.is_not(None)

    case "in":
      return column.in_(filters.in_value or [])

    case "nin":
      return column.not_in(filters.in_value or [])

    case "between":
      return column.between(filters.start, filters.end)

    case _:
      raise ValueError(f"Unsupported operator: {filters.op}")
















