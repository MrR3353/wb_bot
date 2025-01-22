from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes import router
from app.services.scheduler import scheduler

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()


app.include_router(router)
