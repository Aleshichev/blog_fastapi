from fastapi import FastAPI, Request
from .config import (
    SWAGGER_PARAMETERS,
    PROJECT_NAME,
    API_PREFIX,
)
from sqladmin import Admin
from src.author.routers import authors_router

from src.post.routers import posts_router
from src.category.routers import categories_router
from src.tag.routers import tags_router

app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title=PROJECT_NAME,
)

api_routers = [
    authors_router,
    tags_router,
    categories_router,
    posts_router,
]


[app.include_router(router, prefix=API_PREFIX) for router in api_routers]
