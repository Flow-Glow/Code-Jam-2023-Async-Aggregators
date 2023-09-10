import numpy as np
from PIL import Image
from PyQt6.QtGui import QImage, QPixmap

from lib.double_exposure.double_exposure import double_exposure
from src.utils.lru_cache_pil import LRUCachePIL

# Create a cache for storing images:
_image_cache = LRUCachePIL(capacity=10)  # Cache capacity of 10 images


def apply_double_exposure(
    img1: tuple, img2: tuple, slider_value: int, w: int, h: int
) -> QPixmap:
    """
    Apply double exposure to an image

    :param img1:
    :param img2:
    :param slider_value:
    :param w: width of the image label
    :param h: height of the image label
    :return:
    """
    img1_path = str(img1)
    if not (_img := _image_cache.get(img1_path)):
        _img = Image.open(img1_path)
        _image_cache.put(img1_path, _img)
    img1 = _img

    img2_path = str(img2)
    if not (_img := _image_cache.get(img2_path)):
        _img = Image.open(img2_path)
        _image_cache.put(img2_path, _img)
    img2 = _img

    # Convert slider value to float between 0 and 1
    adjusted_slider_value = float(slider_value * 5) / 100

    # Apply double exposure
    blended_image = double_exposure(img1, img2, adjusted_slider_value)

    # Convert blended image to QPixmap
    image_np = np.array(blended_image)
    height, width, channel = image_np.shape
    bytesPerLine = 3 * width
    qimage = QImage(
        image_np.data, width, height, bytesPerLine, QImage.Format.Format_RGB888
    )
    pixmap = QPixmap.fromImage(qimage)
    pixmap = pixmap.scaled(w, h)
    return pixmap
