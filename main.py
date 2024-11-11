import uvicorn
from fastapi import FastAPI

from api_v1.views import router as image_router

app = FastAPI()
app.include_router(image_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
