from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QComboBox, QFrame, QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout,
    QWidget
)


class NoDragSlider(QSlider):
    """QSlider subclass to disable dragging."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(NoDragSlider, self).__init__(*args, **kwargs)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Suppress the mouseMoveEvent to disable dragging."""
        event.ignore()


class ControlPanel(QWidget):
    """Control Panel"""

    # Define a new signal at the top of the class
    sliderValueChanged = pyqtSignal(str, int)
    comboBoxesSwapped = pyqtSignal(str, str)

    def __init__(self, title: str, widget_info: dict):
        super().__init__()
        layout = QVBoxLayout(self)
        self.title = title
        self.combo_boxes = []

        title_box = self.create_panel_title(title)
        layout.addWidget(title_box)

        for info in widget_info.get('sliders', []):
            label, slider_range, orientation, disable_mouse_drag = info
            layout.addWidget(QLabel(label))
            if disable_mouse_drag:
                slider = NoDragSlider(orientation)
            else:
                slider = QSlider(orientation)
            slider.setMinimum(0)
            slider.setMaximum(20)
            slider.setTickInterval(1)
            slider.setSingleStep(1)  # arrow-key step-size
            slider.setPageStep(1)  # mouse-wheel/page-key step-size
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.valueChanged.connect(lambda value, lbl=label: self.forward_signal(lbl, value))
            slider_frame = self.style_slider(slider, slider_range, orientation == Qt.Orientation.Horizontal)
            slider_frame.setMaximumHeight(45)
            layout.addWidget(slider_frame)

        # Adding dropdowns
        for info in widget_info.get('dropdowns', []):
            combo_box1 = QComboBox()
            combo_box2 = QComboBox()

            combo_box1.addItems(info)
            combo_box2.addItems(info)

            layout.addWidget(combo_box1)
            layout.addWidget(combo_box2)

            # Append the QComboBoxes to the list
            self.combo_boxes.append((combo_box1, combo_box2))

        # Adding buttons
        for _ in widget_info.get('buttons', []):
            button = QPushButton()
            button.setText("swap")

            # Use default arguments in the lambda to capture the current values of combo_box1 and combo_box2
            # Assuming one button per pair of dropdowns.
            cb1, cb2 = self.combo_boxes.pop(0)  # Pop the first pair of QComboBoxes from the list
            button.clicked.connect(lambda checked, cb1=cb1, cb2=cb2: self.grab_values(cb1, cb2))

            layout.addWidget(button)

        layout.addStretch()

    def grab_values(self, combo_box1: QComboBox, combo_box2: QComboBox) -> None:
        """Grab the values from the QComboBoxes and emit the signal"""
        value1 = combo_box1.currentText()
        value2 = combo_box2.currentText()
        self.comboBoxesSwapped.emit(value1, value2)

    def forward_signal(self, label: str, value: int) -> None:
        """
        Forward the signal from the slider to the main window

        :param label:
        :param value:
        :return:
        """
        # Emit the new signal
        self.sliderValueChanged.emit(label, value)

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

        title = QLabel(name)
        title.setStyleSheet("font-size: 22px")

        title_centre.addWidget(QLabel())
        title_centre.addWidget(title)
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

            "QSlider::handle:horizontal {"
            "background-color: gray;"
            "width: 20px;"
            "border-radius: 3px; }"

            "QSlider::handle:vertical {"
            "background-color: black;"
            "height: 20px;"
            "border-radius: 3px; }"
        )

        if horizontal:
            slider_layout = QHBoxLayout(slider_frame)
        else:
            slider_layout = QVBoxLayout(slider_frame)

        slider_layout.addWidget(QLabel(str(range_value[0])))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel(str(range_value[-1])))

        return slider_frame