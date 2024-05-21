from typing import Type, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from sqlalchemy import select, update, delete
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status, Response, UploadFile, File, BackgroundTasks
from .exceptions import NO_DATA_FOUND, SERVER_ERROR, NO_RECORD, SUCCESS_DELETE
from .schemas import AuthorCreateSchema, AuthorUpdateSchema
from src.author.utils import save_photo, update_photo, delete_photo

async def get_all_authors(
    model: Type[Base],
    session: AsyncSession,
):
    try:
        query = select(model).order_by(model.id)
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


async def get_author_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return response


async def create_author(
    author_data: AuthorCreateSchema,
    model: Type[Base],
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    # file.filename = f"{uuid.uuid4()}.jpg"
    # contents = await file.read()
    
    # with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
    #     f.write(contents)
    author_data.photo = await save_photo(author_data.photo, model, background_tasks)

    try:
        author = model(name=author_data.name, email=author_data.email, photo=author_data.photo)
        session.add(author)
        await session.commit()
        return author
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

async def update_author(
    author_data: AuthorUpdateSchema,
    model: Type[Base],
    session: AsyncSession,
    author_id: int,
    background_tasks: BackgroundTasks,
    photo: Optional[UploadFile],
):
    query = select(model).where(model.id == author_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    update_data = author_data.model_dump(exclude_none=True)
    if photo:
        update_data["photo"] = await update_photo(
            photo, record, "photo", background_tasks
        )
    if not update_data:
        return Response(status_code=204)
    try:
        query = (
            update(model)
            .where(model.id == author_id)
            .values(**update_data)
            .returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_author_by_id(
    background_tasks: BackgroundTasks,
    author_id: int,
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(model.id == author_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    try:
        query = delete(model).where(model.id == author_id)
        await session.execute(query)
        await session.commit()
        await delete_photo(record.photo, background_tasks)
        return {"message": SUCCESS_DELETE % author_id}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
