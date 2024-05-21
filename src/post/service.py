from sqlalchemy.ext.asyncio import AsyncSession
from src.post.models import Post, PostTag
from src.post.schemas import CreatePostSchema
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

# async def create_post(session: AsyncSession, post_data: CreatePostSchema) -> Post:
#     post = Post(
#         title=post_data.title,
#         content=post_data.content,
#         author_id=post_data.author_id,
#         category_id=post_data.category_id
#     )
#     session.add(post)
#     await session.commit()
#     return post


async def create_post(
    session: AsyncSession,
    post_data: CreatePostSchema) -> Post:
    try:
        # Создаем новый пост
        post = Post(
            title=post_data.title,
            content=post_data.content,
            author_id=post_data.author_id,
            category_id=post_data.category_id
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)  # Обновление объекта post, чтобы получить его ID

        # Связываем пост с тегами
        if post_data.tag_ids:
            for tag_id in post_data.tag_ids:
                post_tag = PostTag(post_id=post.id, tag_id=tag_id)
                session.add(post_tag)
            await session.commit()

        return post
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
