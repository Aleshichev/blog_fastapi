from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from .service import (
    get_all_posts,
    create_post,
    get_post_by_id,
    patch_post,
    delete_post_by_id,
)

from fastapi import APIRouter, Depends

from src.models import Post
from .schemas import (
    PostCreateSchema,
    PostPatchSchema,
    PostBaseSchema,
    PostTagCreatedSchema,
    TagPatchSchema,
)

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
async def create_post_route(
    post_data: PostCreateSchema = Depends(PostCreateSchema.as_form),
    post_tag_data: PostTagCreatedSchema = Depends(PostTagCreatedSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_post(post_data, Post, session, post_tag_data)


@posts_router.patch("/{post_id}")
async def update_post_route(
    post_id: int,
    post_data: PostPatchSchema = Depends(PostPatchSchema.as_form),
    post_tag_data: TagPatchSchema = Depends(TagPatchSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await patch_post(post_id, post_data, Post, session, post_tag_data)


@posts_router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_post_by_id(post_id, Post, session)
