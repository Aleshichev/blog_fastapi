from pydantic import BaseModel, Field
from fastapi import Form


class AuthorBaseSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=100)


class AuthorCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=100)
  
    @classmethod
    def as_form(
        cls,
        name: str = Form(max_length=50),
        email: str = Form(max_length=100),
    ):
        return cls(name=name, email=email)
class AuthorUpdateSchema(AuthorCreateSchema):
    pass
