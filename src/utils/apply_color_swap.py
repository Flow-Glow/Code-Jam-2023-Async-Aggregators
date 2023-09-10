# Now integrate the LRUCache into your previous function:
from PIL import Image
from PyQt6.QtGui import QImage, QPixmap

from lib.pixelate_and_swap.pixelate_and_swap import swap_colors
from src.utils.apply_double_exposure import LRUCachePIL

_image_cache = LRUCachePIL(capacity=10)  # Cache capacity of 10 images


def apply_color_swap(
    image: tuple, first_color: str, second_color: str, w: int, h: int
) -> QPixmap:
    """
    Apply color swap to an image

    :param image: Path to image
    :param first_color:
    :param second_color:
    :param w: width of the image label
    :param h: height of the image label
    :return: QPixmap
    """
    colors = {
        "Rust": (164, 43, 17),
        "Chocolate": (229, 95, 24),
        "Flamenco": (236, 135, 67),
        "Casablanca": (238, 171, 98),
        "Buff": (242, 217, 143),
    }
    img_path = str(image)
    if not (_img := _image_cache.get(img_path)):
        _img = Image.open(img_path)
        _image_cache.put(img_path, _img)
    img = _img

    img = img.convert("RGB")

    first_color_tuple = colors[first_color]
    second_color_tuple = colors[second_color]

    # Apply color swap
    swapped_image = swap_colors(img, first_color_tuple, second_color_tuple)

    # Convert swapped PIL image to QPixmap
    swapped_image = swapped_image.convert("RGBA")
    data = swapped_image.tobytes("raw", "BGRA")
    qim = QImage(
        data, swapped_image.size[0], swapped_image.size[1], QImage.Format.Format_ARGB32
    )
    pixmap = QPixmap.fromImage(qim)
    pixmap = pixmap.scaled(w, h)
    return pixmap
