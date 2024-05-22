from pydantic import BaseModel, Field
from fastapi import Form


class CategoryBaseSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(None, max_length=255)


class CategoryCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(None, max_length=255)

    @classmethod
    def as_form(
        cls,
        name: str = Form(max_length=50),
        description: str = Form(max_length=255),
    ):
        return cls(name=name, description=description)


class CategoryUpdateSchema(CategoryCreateSchema):
    pass
