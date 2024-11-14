from datetime import datetime

from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: int
    title: str
    path: str
    uploaded_at: datetime
    resolution: str
    size: int

    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str
