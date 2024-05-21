from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from .exceptions import NO_DATA_FOUND, SERVER_ERROR


async def get_all_authors(
    model: Type[Base],
    session: AsyncSession,
):
    try:
        query = select(model)
        author = await session.execute(query)
        response = author.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
