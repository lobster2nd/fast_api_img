from datetime import date

from pydantic import BaseModel


class UploadImage(BaseModel):
    title: str
    path: str
    uploaded_at: date
    resolution: str
    size: int
