import os
import uuid

from PIL import Image
from fastapi import UploadFile


ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/bmp",
                      "image/tiff"}


def is_image(file: UploadFile) -> bool:
    """Проверка, что получен именно файл изображения"""

    if file.content_type not in ALLOWED_MIME_TYPES:
        return False

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg',
                                           '.gif', '.bmp', '.tiff')):
        return False

    return True


def get_unique_filename(filename: str) -> str:
    """Генерация уникального имя файла, добавляя UUID"""

    base_name, ext = os.path.splitext(filename)
    unique_name = f"{base_name}_{str(uuid.uuid4())[:7]}{ext}"
    return unique_name


def get_image_resolution(image: str) -> str:
    """Замер разрешения изображения"""

    with Image.open(image) as img:
        width, height = img.size
        resolution = f"{width}x{height}"

    return resolution


def resize_image(image: str, width: int, height: int) -> None:
    """Изменение размера изображения"""

    base_name, ext = os.path.splitext(image)

    img = Image.open(image)
    img.resize((width, height))
    img_path = f'{base_name}_{width}x{height}{ext}'
    img.save(img_path)

