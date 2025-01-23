from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_session
from app.schemas import ProductSchema
from app.services.auth import verify_token
from app.services.scheduler import schedule_product_collection
from app.services.wb_api import get_product as get_product_from_wb

router = APIRouter(prefix='/api/v1', tags=['Products'])


@router.post("/products", dependencies=[Depends(verify_token)])
async def get_product(artikul: str, session: AsyncSession = Depends(get_session)) -> ProductSchema | None:
    product = await get_product_from_wb(artikul)
    if product is None:
        return None
    return await crud.upsert_product(session, product)


@router.get("/subscribe/{artikul}", dependencies=[Depends(verify_token)])
async def subscribe_product(artikul: str) -> dict:
    schedule_product_collection(artikul)
    return {"message": f"Subscription started for artikul {artikul}"}
