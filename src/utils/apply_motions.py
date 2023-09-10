from PyQt6.QtGui import QImage, QPixmap

from lib.motions.motions import MotionTransformer


def apply_motion(args: dict) -> QPixmap:
    """
    Apply a motion to an image

    :param args: a dictionary of arguments
    :return: QPixmap of the image
    """
    mt: MotionTransformer = args["MotionTransformer"]
    try:
        image = mt.calculate_output(
            (
                args.get("horizontal wave", 0),
                args.get("vertical wave", 0),
                args.get("vertical spike", 0),
                args.get("horizontal spike", 0),
                args.get("explode", 0),
            )
        )
        image = image.convert("RGBA")
        data = image.tobytes("raw", "BGRA")
        qim = QImage(data, image.size[0], image.size[1], QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        pixmap = pixmap.scaled(args["image_label_w"], args["image_label_h"])
        return pixmap
    except Exception as e:
        print(e)
        return QPixmap()
