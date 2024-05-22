from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from .exceptions import NO_DATA_FOUND, SERVER_ERROR, NO_RECORD, SUCCESS_DELETE
from .schemas import PostCreateSchema, PostUpdateSchema, PostTagCreatedSchema
from src.models import post_tags


async def get_all_posts(
    model: Type[Base],
    session: AsyncSession,
):
    try:
        query = select(model).order_by(model.id)
        post = await session.execute(query)
        response = post.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def get_post_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_post(
    post_data: PostCreateSchema,
    model: Type[Base],
    session: AsyncSession,
    post_tag_data: PostTagCreatedSchema,
):
    try:
        post = model(
            title=post_data.title,
            content=post_data.content,
            author_id=post_data.author_id,
            category_id=post_data.category_id,
        )

        session.add(post)
        await session.flush()
        print(post_tag_data)
        for tag_id in post_tag_data.tag_id:
            post_tag_instance = post_tags.insert().values(
                post_id=post.id, tag_id=tag_id
            )
            await session.execute(post_tag_instance)

        await session.commit()

        return post
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
