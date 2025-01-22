from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Product


async def get_product_by_article(session: AsyncSession, article: str) -> Product:
    result = await session.execute(select(Product).where(Product.article == article))
    return result.scalars().first()


async def create_product(session: AsyncSession, product_data: dict) -> Product:
    product = Product(**product_data)
    session.add(product)
    await session.commit()
    return product
