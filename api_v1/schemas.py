from datetime import date

from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: int
    title: str
    path: str
    uploaded_at: date
    resolution: str
    size: int

    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str
