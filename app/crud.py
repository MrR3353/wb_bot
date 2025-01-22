from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.models import Product
from app.schemas import ProductSchema


async def get_product_by_article(session: AsyncSession, article: str) -> Product:
    result = await session.execute(select(Product).where(Product.article == article))
    return result.scalars().first()


async def upsert_product(session: AsyncSession, product_schema: ProductSchema) -> Product:
    stmt = insert(Product).values(**product_schema.dict()).on_conflict_do_update(
        index_elements=['article'],
        set_=product_schema.dict()
    ).returning(Product)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalars().first()

