from fastapi import FastAPI, Request
from .config import SWAGGER_PARAMETERS, PROJECT_NAME, API_PREFIX

# from src.utils import lifespan
from src.author.routers import authors_router


app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title=PROJECT_NAME,
    # lifespan=lifespan,
)

api_routers = [
    authors_router,
]

[app.include_router(router, prefix=API_PREFIX) for router in api_routers]
