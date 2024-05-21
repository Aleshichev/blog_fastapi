from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from .service import (
    get_all_tags,
    create_tag,
    get_tag_by_id,
    update_tag,
    delete_tag_by_id,
)

from fastapi import APIRouter, Depends

from src.models import Tag
from .schemas import TagCreateSchema, TagUpdateSchema, TagBaseSchema

tags_router = APIRouter(prefix="/tags", tags=["Tags"])


@tags_router.get("", response_model=List[TagBaseSchema])
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    records = await get_all_tags(Tag, session)
    return records


@tags_router.get("/{id}", response_model=TagBaseSchema)
async def get_tag(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_tag_by_id(Tag, session, id)


@tags_router.post(
    "",
)
async def create_tag_route(
    tag_data: TagCreateSchema = Depends(TagCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_tag(tag_data, Tag, session)


@tags_router.put("/{tag_id}", response_model=TagBaseSchema)
async def update_tag_by_id(
    tag_id: int,
    tag_data: TagUpdateSchema = Depends(TagUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await update_tag(tag_data, Tag, session, tag_id)


@tags_router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_tag_by_id(tag_id, Tag, session)
