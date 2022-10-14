# build a schema using pydantic
from pydantic import BaseModel


class Item(BaseModel):
    product: str
    quantity: int
    price: float
    location: str
    status: str
    magazine_id: int

    class Config:
        orm_mode = True


class Magazine(BaseModel):
    name: str
    description: str
    avatar: str
    location: str

    class Config:
        orm_mode = True
