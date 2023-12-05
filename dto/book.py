from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    publish_year: str
    isbn: str
