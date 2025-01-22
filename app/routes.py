from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import ProductSchema
from app.services.wb_api import get_product as get_product_info
from app import crud

router = APIRouter(prefix='/api/v1', tags=['Products'])


@router.post("/products")
async def get_product(artikul: str, session: AsyncSession = Depends(get_session)) -> ProductSchema | None:
    product = await get_product_info(artikul)
    if product is None:
        return None
    return await crud.upsert_product(session, product)
