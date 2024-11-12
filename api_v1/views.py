import os
import shutil
from fastapi import APIRouter, File, UploadFile

from api_v1.schemas import UploadImage
from api_v1.utils import get_unique_filename,resize_image

router = APIRouter(prefix="/images")


@router.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    """Загрузка изображения"""

    img_dir = 'uploaded_images'
    os.makedirs(img_dir, exist_ok=True)

    img_name = get_unique_filename(image.filename)
    img_path = os.path.join(img_dir, img_name)

    with open(img_path, 'wb') as origin:
        shutil.copyfileobj(image.file, origin)

    resize_image(img_path, 100, 100)
    resize_image(img_path, 500, 500)

    return {'message': 'ok'}
