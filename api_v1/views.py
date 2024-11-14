import os
import shutil
from datetime import datetime

from fastapi import APIRouter, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.models import Image
from api_v1.utils import get_unique_filename, resize_image
from core.database import db_helper

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

    session: AsyncSession = await db_helper.get_session()

    new_image = Image(
        title=image.filename,
        path=img_path,
        uploaded_at=datetime.now(),
        resolution='100x100',
        size=os.path.getsize(img_path)
    )
    async with session:
        session.add(new_image)
        await session.commit()
        await session.refresh(new_image)

    return new_image
