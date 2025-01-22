from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    article = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
