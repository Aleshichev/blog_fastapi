from datetime import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.database import Base
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from .exceptions import NO_DATA_FOUND, SERVER_ERROR, NO_RECORD, SUCCESS_DELETE
from .schemas import PostCreateSchema, PostPatchSchema, PostTagCreatedSchema, TagPatchSchema
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


async def patch_post(
    post_id: int,
    post_data: PostPatchSchema,
    model: Type[Base],
    session: AsyncSession,
    post_tag_data: TagPatchSchema,
):
    try:
        post = await get_post_by_id(model, session, post_id)
        
        if post_data.title:
            post.title = post_data.title
        if post_data.content:
            post.content = post_data.content
        if post_data.author_id:
            post.author_id = post_data.author_id
        if post_data.category_id:
            post.category_id = post_data.category_id
        
        post.created_at = datetime.now()

        if post_data.created_at:
            post.created_at = post_data.created_at
    
            
        
     
        await session.execute(post_tags.delete().where(post_tags.c.post_id == post_id))
        
        if post_tag_data.tag_id:
        
            for tag_id in post_tag_data.tag_id:
                await session.execute(post_tags.insert().values(post_id=post_id, tag_id=tag_id))
        
        await session.commit()
        
        return post
    except IntegrityError as e:
        await session.rollback()

        raise HTTPException(status_code=400, detail="Foreign key violation error: tag_id does not exist")
    except HTTPException as e:
        await session.rollback()
        raise e



async def delete_post_by_id(
    post_id: int,
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(model.id == post_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    
    try:
        await session.execute(post_tags.delete().where(post_tags.c.post_id == post_id))
        await session.execute(model.__table__.delete().where(model.id == post_id))
        
        await session.commit()
        
        return {"detail": "Post and associated tags deleted successfully"}
    except HTTPException as e:
        await session.rollback()
        raise e