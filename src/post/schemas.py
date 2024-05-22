from pydantic import BaseModel, Field
from fastapi import Form, UploadFile, File
from typing import List, Optional, Union
from datetime import datetime


class PostBaseSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)
    author_id: int = Field(..., ge=1, le=6)
    category_id: int = Field(..., ge=1, le=6)
    created_at: datetime = Field(default_factory=datetime.now)


class PostCreateSchema(PostBaseSchema):
    @classmethod
    def as_form(
        cls,
        title: str = Form(max_length=100),
        content: str = Form(max_length=2000),
        author_id: int = Form(),
        category_id: int = Form(),
        created_at: Optional[datetime] = Form(default=None),        
    ):
        if created_at is None:
            created_at = datetime.now()
        return cls(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category_id,
            created_at=created_at
        )


class PostUpdateSchema(PostBaseSchema):
    pass


class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


    
class PostTagCreatedSchema(BaseModel):
    tag_id: List[int] = Field(..., min_items=1, max_items=6,)
    
    @classmethod
    def as_form(
        cls,
        tag_id: Union[str, List[int]] = Form(),
    ):
        if isinstance(tag_id, str):
            tag_id = tag_id.split(',')
            tag_id = [int(tag.strip()) for tag in tag_id if tag.isdigit()]

        return cls(tag_id=tag_id)
