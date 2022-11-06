from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserIn(User):
    password: str


class UserOut(User):
    id: int


class UserInDB(UserOut):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class Magazine(BaseModel):
    id: int
    name: str
    description: str
    avatar: str
    location: str
    date_of_creation: str
