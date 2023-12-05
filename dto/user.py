from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str
