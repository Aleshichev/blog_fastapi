from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from .service import (
    get_all_posts,
    create_post,
    get_post_by_id,
    # update_tag,
    # delete_tag_by_id,
)

from fastapi import APIRouter, Depends

from src.models import Post
from .schemas import PostCreateSchema, PostUpdateSchema, PostBaseSchema, PostTagCreatedSchema

posts_router = APIRouter(prefix="/posts", tags=["Posts"])


@posts_router.get("", response_model=List[PostBaseSchema])
async def get_posts(session: AsyncSession = Depends(get_async_session)):
    records = await get_all_posts(Post, session)
    return records


@posts_router.get("/{id}", response_model=PostBaseSchema)
async def get_post(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_post_by_id(Post, session, id)


@posts_router.post(
    "",
)
async def create_tag_route(
    post_data: PostCreateSchema = Depends(PostCreateSchema.as_form),
    post_tag_data: PostTagCreatedSchema = Depends(PostTagCreatedSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_post(post_data, Post, session, post_tag_data)


# @tags_router.put("/{tag_id}", response_model=TagBaseSchema)
# async def update_tag_by_id(
#     tag_id: int,
#     tag_data: TagUpdateSchema = Depends(TagUpdateSchema.as_form),
#     session: AsyncSession = Depends(get_async_session),
# ):
#     return await update_tag(tag_data, Tag, session, tag_id)


# @tags_router.delete("/{tag_id}")
# async def delete_tag(
#     tag_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     return await delete_tag_by_id(tag_id, Tag, session)
