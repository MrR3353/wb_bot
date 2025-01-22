import time

from pydantic import BaseModel


class ProductSchema(BaseModel):
    article: str
    name: str
    price: float
    rating: float
    stock: int
