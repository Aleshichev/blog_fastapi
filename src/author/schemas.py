from pydantic import BaseModel


class GetAuthorSchema(BaseModel):
    name: str
