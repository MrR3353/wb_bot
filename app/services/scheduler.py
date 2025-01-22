from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.config
from app.crud import upsert_product
from app.database import DATABASE_URL, get_session
from app.services.wb_api import get_product

jobstore = SQLAlchemyJobStore(url=DATABASE_URL.replace("asyncpg", "psycopg2"))  # use sync connection
scheduler = AsyncIOScheduler(jobstores={"default": jobstore})


async def periodic_product_collection(article: str):
    async for session in get_session():
        product = await get_product(article)
        if product is not None:
            return await upsert_product(session, product)


def schedule_product_collection(article: str):
    scheduler.add_job(
        periodic_product_collection,
        "interval",
        minutes=app.config.settings.SCHEDULER_INTERVAL,
        args=[article],
        id=f"product-{article}",
        replace_existing=True
    )