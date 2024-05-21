from pydantic import BaseModel, Field
from fastapi import Form


class TagBaseSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)


class TagCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

  
    @classmethod
    def as_form(
        cls,
        name: str = Form(max_length=50),

    ):
        return cls(name=name)
class TagUpdateSchema(TagCreateSchema):
    pass
