from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
)

from src.Utils.apply_color_swap import apply_color_swap
from src.Utils.apply_double_exposure import apply_double_exposure
from src.Utils.apply_motions import apply_motion
from src.Utils.apply_unmask_reverse_ishihara import (
    apply_unmask_reverse_ishihara
)


class Filter(QWidget):
    """Filter"""

    # Define a custom signal to be emitted when any slider changes its value
    sliderValueChanged = pyqtSignal(str, int)

    def __init__(self, name: str, sliders_info: list):
        """Init"""
        super().__init__()

        self.name = name
        self.sliders = {}  # Dictionary to store sliders with their labels as keys

        layout = QVBoxLayout(self)

        title_box = self.create_panel_title(name)
        layout.addWidget(title_box)

        for slider_label, slider_range, slider_orientation in sliders_info:
            layout.addWidget(QLabel(slider_label))
            slider = QSlider(slider_orientation)
            slider.setRange(*slider_range)
            slider.valueChanged.connect(lambda value, lbl=slider_label: self._on_slider_value_changed(lbl, value))
            slider_frame = self.style_slider(slider, slider_range, slider_orientation == Qt.Orientation.Horizontal)
            layout.addWidget(slider_frame)

            self.sliders[slider_label] = slider

        layout.addStretch()

    def _on_slider_value_changed(self, label: str, value: int) -> None:
        """
        Forward the signal from the slider to the main window

        :param label:
        :param value:
        :return:
        """
        self.sliderValueChanged.emit(label, value)

    def get_slider_value(self, label: str) -> int:
        """
        Get the value of a slider

        :param label:
        :return:
        """
        return self.sliders[label].value()

    @staticmethod
    def create_panel_title(name: str) -> QFrame:
        """
        Stylised control panel title for consistency

        :param name:
        :return: QFrame panel title
        """
        title_box = QFrame()
        object_name = "_".join(name.lower().split())
        title_box.setObjectName(object_name + "_box")
        title_box.setMinimumSize(200, 0)
        title_box.setStyleSheet(
            f"QFrame#{object_name + '_box'}"
            "{ border: 1px solid 'black'; "
            "border-radius: 6px; "
            "background-color: 'white'; }"
        )

        title_centre = QHBoxLayout(title_box)
        title_label = QLabel(name)
        title_label.setStyleSheet("font-size: 22px")
        title_centre.addWidget(QLabel())
        title_centre.addWidget(title_label)
        title_centre.addWidget(QLabel())

        return title_box

    @staticmethod
    def style_slider(slider: QSlider, range_value: tuple, horizontal: bool) -> QFrame:
        """
        Style PyQt6 sliders for consistency

        :param range_value:
        :param slider:
        :param slider, range_value, horizontal:
        :return: QFrame slider
        """
        slider_frame = QFrame()
        slider_frame.setObjectName("sliderframe")
        slider_frame.setStyleSheet(
            "QFrame#sliderframe { "
            "border: 1px solid 'black';"
            "border-radius: 6px;"
            "background-color: 'white'; }"
        )

        slider_layout = (
            QHBoxLayout(slider_frame) if horizontal else QVBoxLayout(slider_frame)
        )
        slider_layout.addWidget(QLabel(str(range_value[0])))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel(str(range_value[-1])))

        return slider_frame


def apply_filter(filter_name: str, args: dict) -> QPixmap:
    """
    Apply a filter to an image

    :param filter_name:
    :param args:
    :return: img
    """
    if filter_name == "Double Exposure":
        args_for_filter = {}
        for key, value in args.items():
            if key == "Exposure":
                args_for_filter["Exposure"] = value
            if key == "image_to_edit":
                args_for_filter["image_to_edit"] = value
            if key == "second_image":
                args_for_filter["second_image"] = value

        new_img = apply_double_exposure(
            args_for_filter["image_to_edit"],
            args_for_filter["second_image"],
            args_for_filter["Exposure"]
        )
        return new_img
    if filter_name == "Ishihara":
        args_for_filter = {}
        for key, value in args.items():
            if key == "A":
                args_for_filter["A"] = value
            if key == "B":
                args_for_filter["B"] = value
            if key == "image_to_edit":
                args_for_filter["image_to_edit"] = value
        new_img = apply_unmask_reverse_ishihara(
            args_for_filter
        )
        return new_img
    if filter_name == "Color Swap":
        args_for_filter = {}

        for key, value in args.items():
            if key == "first_color":
                args_for_filter["first_color"] = value
            if key == "second_color":
                args_for_filter["second_color"] = value
            if key == "image_to_edit":
                args_for_filter["image_to_edit"] = value
        new_img = apply_color_swap(
            args_for_filter["image_to_edit"],
            args_for_filter["first_color"],
            args_for_filter["second_color"]
        )
        return new_img
    if filter_name == "Motion":
        args_for_filter = {}
        for key, value in args.items():
            if key == "horizontal wave":
                args_for_filter["horizontal wave"] = value
            elif key == "vertical wave":
                args_for_filter["vertical wave"] = value
            elif key == "horizontal spike":
                args_for_filter["horizontal spike"] = value
            elif key == "vertical spike":
                args_for_filter["vertical spike"] = value
            elif key == "MotionTransformer":
                args_for_filter["MotionTransformer"] = value
        new_img = apply_motion(args_for_filter)
        return new_img
    pass
