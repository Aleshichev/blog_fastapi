from pydantic import BaseModel, Field, EmailStr
from fastapi import Form, UploadFile, File


class AuthorBaseSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    photo: str = Field(..., max_length=500)


class AuthorCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    photo: UploadFile

    @classmethod
    def as_form(
        cls,
        photo: UploadFile,
        name: str = Form(max_length=50),
        email: EmailStr = Form(),
    ):
        return cls(name=name, email=email, photo=photo)


class AuthorUpdateSchema(AuthorCreateSchema):
    pass
