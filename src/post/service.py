from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from .exceptions import NO_DATA_FOUND, SERVER_ERROR

