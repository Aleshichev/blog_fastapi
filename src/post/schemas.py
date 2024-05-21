from pydantic import BaseModel
from typing import List

class CreatePostSchema(BaseModel):
    title: str
    content: str
    author_id: int
    category_id: int
    tag_ids: List[int]

    class Config:
        orm_mode = True
