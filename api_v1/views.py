import os
import shutil
from fastapi import APIRouter, File, UploadFile

from api_v1.schemas import UploadImage

router = APIRouter(prefix="/images")


@router.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    """Загрузка изображения"""

    os.makedirs('uploaded_images', exist_ok=True)
    file_path = os.path.join('uploaded_images', image.filename)

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'image': image.filename}
