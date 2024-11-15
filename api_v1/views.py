import os
import shutil
from datetime import datetime
from typing import List

from fastapi import APIRouter, File, UploadFile, HTTPException, Query, \
    Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.models import Image
from api_v1.schemas import ImageResponse, ErrorResponse, ImageUpdate
from api_v1.utils import get_unique_filename, resize_image, \
    get_image_resolution, is_image
from core.database import db_helper

router = APIRouter(prefix="/images")


@router.post("/upload/",
             status_code=201,
             responses={
                 201: {'model': ImageResponse},
                 400: {'model': ErrorResponse}
             })
async def upload_image(image: UploadFile = File(...)):
    """Загрузка изображения"""

    if not is_image(image):
        raise HTTPException(status_code=400, detail="Invalid image format")

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
        resolution=get_image_resolution(img_path),
        size=os.path.getsize(img_path)
    )
    async with session:
        session.add(new_image)
        await session.commit()
        await session.refresh(new_image)

    return new_image


@router.get("/all/", response_model=List[ImageResponse],
            responses={
                200: {'model': ImageResponse},
                404: {'model': ErrorResponse}
            })
async def get_all_images():
    """Получение списка всех загруженных изображений"""

    session: AsyncSession = await db_helper.get_session()

    async with session:
        result = await session.execute(select(Image))
        images = result.scalars().all()

        if not images:
            raise HTTPException(status_code=404,
                                detail='Ничего не найдено')

        return images


@router.get("/get/", response_model=ImageResponse,
            responses={
                200: {'model': ImageResponse},
                404: {'model': ErrorResponse}
            })
async def get_image_by_id(image_id: int = Query(...)):
    """Получение изображения по id"""

    session: AsyncSession = await db_helper.get_session()

    async with session:
        result = await session.execute(select(Image)
                                       .filter(Image.id == image_id))
        image = result.scalars().first()

        if not image:
            raise HTTPException(status_code=404,
                                detail='Ничего не найдено')

        return image


@router.patch("/update/", response_model=ImageResponse,
              responses={
                  200: {'model': ImageResponse},
                  404: {'model': ErrorResponse}
              })
async def update_image(image_id: int, image_update: ImageUpdate):
    """Обновление информации об изображении по id"""

    session: AsyncSession = await db_helper.get_session()

    async with session:
        result = await session.execute(select(Image)
                                       .filter(Image.id == image_id))
        image = result.scalars().first()

        if not image:
            raise HTTPException(status_code=404,
                                detail='Изображение не найдено')

        if image_update.title is not None:
            image.title = image_update.title
        await session.commit()
        await session.refresh(image)

    return image


@router.delete("/delete/",
               status_code=204,
               responses={
                204: {'description': 'Image deleted successfully'},
                404: {'model': ErrorResponse}
               })
async def delete_image_by_id(image_id: int = Query(...)):
    """Получение изображения по id"""

    session: AsyncSession = await db_helper.get_session()

    async with session:
        result = await session.execute(select(Image)
                                       .filter(Image.id == image_id))
        image = result.scalars().first()

        if not image:
            raise HTTPException(status_code=404,
                                detail='Изображение не найдено')

        await session.delete(image)
        await session.commit()

        return Response(status_code=204)
