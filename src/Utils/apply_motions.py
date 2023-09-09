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
        if "horizontal wave" in args:
            horizontal_wave = int(args["horizontal wave"]) * 5 / 100
        else:
            horizontal_wave = 0
        if "vertical wave" in args:
            vertical_wave = int(args["vertical wave"]) * 5 / 100
        else:
            vertical_wave = 0
        if "vertical spike" in args:
            vertical_spike = int(args["vertical spike"]) * 5 / 100
        else:
            vertical_spike = 0
        if "horizontal spike" in args:
            horizontal_spike = int(args["horizontal spike"]) * 5 / 100
        else:
            horizontal_spike = 0

        image = mt.calculate_output(
            (horizontal_wave, vertical_wave, vertical_spike, horizontal_spike)
        )
        image = image.convert("RGBA")
        data = image.tobytes("raw", "BGRA")
        qim = QImage(data, image.size[0], image.size[1], QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        pixmap = pixmap.scaled(450, 450)
        return pixmap
    except Exception as e:
        print(e)
        return QPixmap()
