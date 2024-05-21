from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from .service import (
    get_all_categories,
    create_category,
    get_category_by_id,
    update_category,
    delete_category_by_id,
)

from fastapi import APIRouter, Depends

from src.models import Category
from .schemas import CategoryCreateSchema, CategoryUpdateSchema, CategoryBaseSchema

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get("", response_model=List[CategoryBaseSchema])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    records = await get_all_categories(Category, session)
    return records


@categories_router.get("/{id}", response_model=CategoryBaseSchema)
async def get_category(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_category_by_id(Category, session, id)


@categories_router.post(
    "",
)
async def create_category_route(
    category_data: CategoryCreateSchema = Depends(CategoryCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_category(category_data, Category, session)


@categories_router.put("/{category_id}", response_model=CategoryBaseSchema)
async def update_category_by_id(
    category_id: int,
    category_data: CategoryUpdateSchema = Depends(CategoryUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await update_category(category_data, Category, session, category_id)


@categories_router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_category_by_id(category_id, Category, session)
