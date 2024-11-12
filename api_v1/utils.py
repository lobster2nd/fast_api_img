import os
import uuid

from PIL import Image


def get_unique_filename(filename: str) -> str:
    """Генерация уникального имя файла, добавляя UUID"""

    base_name, ext = os.path.splitext(filename)
    unique_name = f"{base_name}_{str(uuid.uuid4())[:7]}{ext}"
    return unique_name


def resize_image(image: str, width: int, height: int) -> None:
    """Изменение размера изображения"""

    base_name, ext = os.path.splitext(image)

    img = Image.open(image)
    img.resize((width, height))
    img_path = f'{base_name}_{width}x{height}{ext}'
    img.save(img_path)
