from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session

router = APIRouter()


@router.post("/api/v1/products")
async def get_product(artikul: str, db: AsyncSession = Depends(get_session)):
    return {"product": artikul}