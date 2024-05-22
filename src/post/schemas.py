from pydantic import BaseModel, Field
from fastapi import Form, UploadFile, File
from typing import List, Optional, Union
from datetime import datetime


class PostBaseSchema(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)
    author_id: int = Field(..., ge=1, le=6)
    category_id: int = Field(..., ge=1, le=6)
    created_at: datetime = Field(default_factory=datetime.now)


class PostCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)
    author_id: int = Field(..., ge=1, le=6)
    category_id: int = Field(..., ge=1, le=6)
    created_at: datetime = Field(default_factory=datetime.now)
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




    
class PostTagCreatedSchema(BaseModel):
    tag_id: List[int] = Field(..., min_items=1, max_items=6,)
    
    @classmethod
    def as_form(
        cls,
        tag_id: Union[str, List[int]] = Form(),
    ):
        if isinstance(tag_id, str):
            tag_str = tag_id.replace(" ", "")
            tag_str = tag_str.split(',')
            tag_new_id = [int(tag) for tag in tag_str if tag.isdigit()]

        return cls(tag_id=tag_new_id)
from typing import Optional

class PostPatchSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=2000)
    author_id: Optional[int] = Field(None, ge=1, le=6)
    category_id: Optional[int] = Field(None, ge=1, le=6)
    created_at: Optional[datetime] = Field(None)

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(None, max_length=100),
        content: Optional[str] = Form(None, max_length=2000),
        author_id: Optional[int] = Form(None),
        category_id: Optional[int] = Form(None),
        created_at: Optional[datetime] = Form(None),        
    ):
        return cls(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category_id,
            created_at=created_at
        )

class TagPatchSchema(BaseModel):
    tag_id: Optional[List[int]] = Field(None, min_items=1, max_items=6)

    @classmethod
    def as_form(
        cls,
        tag_id: Optional[Union[str, List[int]]] = Form(None),
    ):
        tag_new_id = None
        if isinstance(tag_id, str):
            tag_str = tag_id.replace(" ", "")
            tag_str = tag_str.split(',')
            tag_new_id = [int(tag) for tag in tag_str if tag.isdigit()]

        return cls(tag_id=tag_new_id)
