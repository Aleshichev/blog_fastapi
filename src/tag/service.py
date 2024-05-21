from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from sqlalchemy import select, update, delete
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status, Response
from .exceptions import NO_DATA_FOUND, SERVER_ERROR, NO_RECORD, SUCCESS_DELETE
from .schemas import TagCreateSchema, TagUpdateSchema


async def get_all_tags(
    model: Type[Base],
    session: AsyncSession,
):
    try:
        query = select(model).order_by(model.id)
        tag = await session.execute(query)
        response = tag.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def get_tag_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_tag(
    tag_data: TagCreateSchema,
    model: Type[Base],
    session: AsyncSession,
):
    try:
        tag = model(name=tag_data.name)
        session.add(tag)
        await session.commit()
        return tag
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def update_tag(
    tag_data: TagUpdateSchema,
    model: Type[Base],
    session: AsyncSession,
    tag_id: int,
):
    query = select(model).where(model.id == tag_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    update_data = tag_data.model_dump(exclude_none=True)
    if not update_data:
        return Response(status_code=204)
    try:
        query = (
            update(model)
            .where(model.id == tag_id)
            .values(**update_data)
            .returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_tag_by_id(
    tag_id: int,
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(model.id == tag_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    try:
        query = delete(model).where(model.id == tag_id)
        await session.execute(query)
        await session.commit()
        return {"message": SUCCESS_DELETE % tag_id}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
