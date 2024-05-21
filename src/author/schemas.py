from pydantic import BaseModel, Field
from fastapi import Form, UploadFile, File
from src.config import settings



class AuthorBaseSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=100)
    photo: str = Field(..., max_length=500)



class AuthorCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=100)
    photo: UploadFile
  
    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        name: str = Form(max_length=50),
        email: str = Form(max_length=100),
    ):
        return cls(name=name, email=email, photo=photo)
class AuthorUpdateSchema(AuthorCreateSchema):
    pass
