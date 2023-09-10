import cv2
from PyQt6.QtGui import QImage, QPixmap

from lib.reverse_ishihara.reverse_ishihara import unmask_reverse_ishihara
from src.utils.lru_cache_cv2 import LRUCacheCV2

# Create a cache for storing OpenCV images:
_image_cache_cv2 = LRUCacheCV2(capacity=10)  # Cache capacity of 10 images


def apply_unmask_reverse_ishihara(args: dict) -> QPixmap:
    """
    Apply unmask reverse Ishihara to an image

    :param args: dict
    :return: QPixmap
    """
    try:
        if "A" in args:
            slider_a = int(args["A"])
        else:
            slider_a = 0
        if "B" in args:
            slider_b = int(args["B"])
        else:
            slider_b = 0

        img_path = str(args["image_to_edit"])

        # Check if image exists in cache
        cached_image = _image_cache_cv2.get(img_path)
        if cached_image is None:
            # If not in cache, read with OpenCV and store it in cache
            cv2_img = cv2.imread(img_path)
            _image_cache_cv2.put(img_path, cv2_img)
        else:
            cv2_img = cached_image

        # Apply unmask reverse Ishihara with values from sliders
        unmasked_image = unmask_reverse_ishihara(img_path, slider_a, slider_b)

        # Convert the OpenCV BGR image to RGB format
        unmasked_image_rgb = cv2.cvtColor(unmasked_image, cv2.COLOR_BGR2RGB)

        # Convert the numpy array (OpenCV image) to a QImage
        height, width, channel = unmasked_image_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            unmasked_image_rgb.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888,
        )

        # Convert the QImage to QPixmap
        pixmap = QPixmap.fromImage(q_image)
        resized_pixmap = pixmap.scaled(args["image_label_w"], args["image_label_h"])

        return resized_pixmap
    except Exception as e:
        print(e)
        return QPixmap()  # Return an empty QPixmap
