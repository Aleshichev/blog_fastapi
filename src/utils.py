# from fastapi import FastAPI
# from sqlalchemy import func, select

# from src.auth.models import User
# from src.auth.utils import create_user
# from src.config import settings
# from src.database import get_async_session

# async def lifespan(app: FastAPI):
#     async for s in get_async_session():
#         async with s.begin():
#             user_count = await s.scalar(select(func.count()).select_from(User))
#             if user_count == 0:
#                 await create_user(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
#                 break  # Прерываем цикл, так как пользователь создан

#     yield



# async def lifespan(app: FastAPI):
#     await lock.acquire(blocking=True)
#     async for s in get_async_session():
#         async with s.begin():
#             user_count = await s.scalar(select(func.count()).select_from(User))
#             if user_count == 0:
#                 clear_media_path()
#                 await create_user(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)

#     await lock.release()
#     yield