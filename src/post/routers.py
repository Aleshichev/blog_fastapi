from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.post.service import create_post
from src.post.schemas import CreatePostSchema
from src.post.models import Post


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", response_model=CreatePostSchema)
async def create_post_route(
    post_data: CreatePostSchema,
    session: AsyncSession = Depends(get_async_session),
):
  
    return await create_post(session, post_data)