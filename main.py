from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1.models import Base
from api_v1.views import router as image_router
from core.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(image_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
