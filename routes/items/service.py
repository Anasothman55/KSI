import uuid
from typing import Annotated, Any

from fastapi import HTTPException, status
from fastcrud import FastCRUD, JoinConfig, compute_offset, paginated_response
from fastcrud.core.query import joins
from rich import print
from sqlalchemy import String, cast, func, or_, select, insert, delete as sql_delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from core.models import ItemsModel, ItemsVariantModel, item_categories, CategoriesModel, ItemsInventoryModel
from routes.items.schema import (
  ItemsCreateSchema,
  ItemsReadMultiSchema,
  ItemsReadResponseSchema,
  ItemsReadSchema,
  ItemsSchema,
  ItemsUpdateSchema,
)
from routes.shared.func import integrity_error_raise
from routes.varinats.schema import ItemsVariantReadCodeSchema

items_crud = FastCRUD(ItemsModel)

async def create(
  db: AsyncSession, 
  body: ItemsCreateSchema
):
  try:

    category_uids = list(set(body.categories_uid))

    if category_uids:
      result = await db.execute(
        select(CategoriesModel.uid).where(CategoriesModel.uid.in_(category_uids))
      )

      existing_uids = set(result.scalars().all())
      missing_uids = set(category_uids) - existing_uids

      if missing_uids:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Category does not exist: {next(iter(missing_uids))}",
        )


    variant: ItemsVariantModel | None = (await db.execute(select(ItemsVariantModel).where(ItemsVariantModel.uid == body.variant_uid))).scalar_one_or_none()

    if variant is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The variant dose not exist")

    max_number: int = (
      await db.execute(select(func.max(ItemsModel.sku_number)).where(ItemsModel.variant_uid == body.variant_uid))
    ).scalar_one()

    async with db.begin():
      item = ItemsModel(
        **body.model_dump(exclude={'categories_uid'}),
        sku_number= (max_number or 0) + 1
      )

      db.add(item)
      await db.flush()

      if category_uids:
        await db.execute(
          insert(item_categories).values([
            {
              "item_uid": item.uid,
              "category_uid": uids
            }
            for uids in body.categories_uid
          ])
        )

      return item

  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def read(
  db: AsyncSession, 
  uid: uuid.UUID
):

  res: ItemsModel | None = (await db.execute(
    select(ItemsModel)
    .options(
      selectinload(ItemsModel.variant),
      selectinload(ItemsModel.categories).load_only(CategoriesModel.name),
      selectinload(ItemsModel.inventory).load_only(
        ItemsInventoryModel.owner,
        ItemsInventoryModel.condition
      )
    )
    .where(ItemsModel.uid == uid)
  )).scalar_one_or_none()
  
  if res is None:
    raise HTTPException(
      status_code= status.HTTP_404_NOT_FOUND,
      detail="Items not found"
    )

  return {
    "sku":f"{res.variant.sku_code}-{res.sku_number!s:0>6}",
    **ItemsReadSchema.model_validate(res, from_attributes=True).model_dump(),
  }

async def read_multi(
  db: AsyncSession,
  name: str | None = None, 
  page: int  = 1,
  items_per_page: int = 10,
):
  filters = []
  if name is not None:
    filters.append(
      or_(
        ItemsModel.title.ilike(f"%{name}%"),
        ItemsModel.formal_name.ilike(f"%{name}%")
      )
    )

  offset = (page - 1) * items_per_page
  # Total count
  count_stmt = (
      select(func.count())
      .select_from(ItemsModel)
      .where(*filters)
  )

  total_count = await db.scalar(count_stmt)

  sku = func.concat(
    ItemsVariantModel.sku_code,
    "-",
    func.lpad(cast(ItemsModel.sku_number, String), 6, "0"),
  ).label("sku")
  

  res = (await db.execute(
    select(ItemsModel,sku )
    .join( ItemsVariantModel,ItemsModel.variant_uid == ItemsVariantModel.uid,)
    .where(*filters)
    .offset(offset)
    .limit(items_per_page)
  )).all()

  rows = [
    {**ItemsSchema.model_validate(item, from_attributes=True).model_dump(), 'sku': sku}
    for item, sku in res
  ]

  return {
    "data": rows,
    "total_count": total_count,
    "page": page,
    "items_per_page": items_per_page,
    "has_more": offset < total_count
  }

async def update(
  db: AsyncSession, 
  uid: uuid.UUID, 
  body: ItemsUpdateSchema
):
  try:

    category_uids = list(set(body.categories_uid))

    if category_uids:
      result = await db.execute(
        select(CategoriesModel.uid).where(CategoriesModel.uid.in_(category_uids))
      )

      existing_uids = set(result.scalars().all())
      missing_uids = set(category_uids) - existing_uids

      if missing_uids:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Category does not exist: {next(iter(missing_uids))}",
        )


    async with db.begin():

      item: ItemsModel | None = (await db.execute(
        select(ItemsModel)
        .where(ItemsModel.uid == uid)
      )).scalar_one_or_none()

      if item is None:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="The item does not exist",
        )

      update_data = body.model_dump(exclude_unset=True,exclude={"categories_uid"},)

      for field, value in update_data.items():
        setattr(item, field, value)

      if body.categories_uid is not None:
        await db.execute(
          sql_delete(item_categories).where(item_categories.c.item_uid == item.uid)
        )

        if category_uids:
          await db.execute(
            insert(item_categories).values([
              {
                "item_uid": item.uid,
                "category_uid": category_uid,
              }
              for category_uid in body.categories_uid
            ])
          )

        await db.flush()

    return item

  except IntegrityError as e:
    await db.rollback()
    integrity_error_raise(e)

async def delete(
  db: AsyncSession,
  uid: uuid.UUID
):
  pass