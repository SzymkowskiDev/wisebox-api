from pydantic import BaseModel
from typing import Union

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


class UserIn(UserOut):
    password: str


class UserInDB(UserOut):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
#    email: str | None = None

class Magazine(BaseModel):
    id: int
    name: str
    description: str
    avatar: str
    location: str
    date_of_creation: str
