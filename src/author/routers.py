from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from .schemas import GetAuthorSchema
from .models import Author
from .service import get_all_authors


authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.get("", response_model=List[GetAuthorSchema])
async def get_authors(session: AsyncSession = Depends(get_async_session)):
    records = await get_all_authors(Author, session)
    return records
