from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from .service import (
    get_all_authors,
    create_author,
    get_author_by_id,
    update_author,
    delete_author_by_id,
)

from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File

from src.models import Author
from .schemas import AuthorCreateSchema, AuthorUpdateSchema, AuthorBaseSchema

authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.get("", response_model=List[AuthorBaseSchema])
async def get_authors(session: AsyncSession = Depends(get_async_session)):
    records = await get_all_authors(Author, session)
    return records


@authors_router.get("/{id}", response_model=AuthorBaseSchema)
async def get_author(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_author_by_id(Author, session, id)


@authors_router.post(
    "",
)
async def create_author_route(
    background_tasks: BackgroundTasks,
    author_data: AuthorCreateSchema = Depends(AuthorCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_author(author_data, Author, session, background_tasks)


@authors_router.put("/{author_id}", response_model=AuthorBaseSchema)
async def update_author_by_id(
    author_id: int,
    background_tasks: BackgroundTasks,
    author_data: AuthorUpdateSchema = Depends(AuthorUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    photo: Annotated[UploadFile, File()] = None,
):
    return await update_author(
        author_data, Author, session, author_id, background_tasks, photo
    )


@authors_router.delete("/{author_id}")
async def delete_author(
    background_tasks: BackgroundTasks,
    author_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_author_by_id(background_tasks, author_id, Author, session)
