import os
from uuid import uuid4
from typing import Type

import aiofiles
from fastapi import HTTPException, UploadFile, BackgroundTasks


from src.database import Base
from .exceptions import INVALID_PHOTO, OVERSIZE_FILE
from src.config import PHOTO_FORMATS, MAX_FILE_SIZE_MB


async def save_photo(
    file: UploadFile,
    model: Type[Base],
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:

    if not is_file and file.content_type not in PHOTO_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
        )
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=OVERSIZE_FILE)

    folder_path = os.path.join(
        "static", "media", model.__tablename__.lower().replace(" ", "_")
    )
    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid4().hex}.{file_extension}"
    file_path = os.path.join(folder_path, file_name)

    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file content: {e}")

    async def _save_photo(file_path: str, content: bytes):
        try:
            os.makedirs(folder_path, exist_ok=True)
            async with aiofiles.open(file_path, "wb") as buffer:
                await buffer.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    background_tasks.add_task(_save_photo, file_path, content)
    return file_path


async def delete_photo(path: str, background_tasks: BackgroundTasks) -> None:
    if "media" in path:
        path_exists = os.path.exists(path)
        if path_exists:
            background_tasks.add_task(os.remove, path)


async def update_photo(
    file: UploadFile,
    record: Type[Base],
    field_name: str,
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:
    old_photo_path = getattr(record, field_name, None)
    new_photo = await save_photo(file, record, background_tasks, is_file)
    if old_photo_path:
        await delete_photo(old_photo_path, background_tasks)
    return new_photo
