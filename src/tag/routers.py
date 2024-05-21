from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from .schemas import GetAuthorSchema
from .models import Tag
from .service import get_all_authors

