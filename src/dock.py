from pathlib import Path
from typing import Callable, Dict

from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedLayout,
    QWidget
)

from src.filter import apply_filter
from src.level import Level


class Dock(QWidget):
    """Dock"""

    # Define a new signal at the top of the class
    controlValueChanged = pyqtSignal(str, int)

    def __init__(self, level: Level, image_label: QLabel, update_secret_code_callback: Callable) -> None:
        super().__init__()

        self.level = level
        self._update_secret_code = update_secret_code_callback
        self.img_label = image_label
        self.filters = []
        self.args_cache: Dict[str, int | str] = {}

        for _, filter_item, args in self.level.filters:
            control_panel = filter_item
            control_panel.sliderValueChanged.connect(
                lambda label, value, cp=control_panel: self.update_args_and_image(
                    cp.title,
                    label,
                    value,
                    {
                        "second_image": args["second_image"],
                        "MotionTransformer": args["MotionTransformer"],
                    },
                )
            )

            # Handle the comboBoxesSwapped signal here
            control_panel.comboBoxesSwapped.connect(
                lambda value1, value2, cp=control_panel: self.button_pressed_with_two_values(
                    cp.title,
                    {
                        "first_color": value1,
                        "second_color": value2,
                    }
                )
            )
            self.filters.append(control_panel)

        layout = self._create_central_dock()
        self.setLayout(layout)

    def _create_central_dock(self) -> QHBoxLayout:
        """Create the central dock layout with filters, inputs and buttons."""
        layout = QHBoxLayout()

        # Add spacers
        spacer = QLabel()
        spacer.setMinimumSize(100, 0)
        layout.addWidget(spacer)

        # Filter controls
        filter_dock = self._create_filter_dock()
        layout.addWidget(filter_dock)

        layout.addWidget(spacer)

        return layout

    def _create_filter_dock(self) -> QWidget:
        """Create the filter dock frame with filter controls."""
        frame = QFrame(self)
        frame.setObjectName("filter_dock_frame")
        frame.setStyleSheet(
            "QFrame#filter_dock_frame {"
            "border: 1px solid 'black';"
            "border-radius: 6px; "
            "background-color: 'white';}"
        )
        layout = QHBoxLayout(frame)

        # Filters
        filters = self._create_filters()
        layout.addLayout(filters)

        # Secret code input field
        self.secret_code_input = QLineEdit()
        self.secret_code_input.setPlaceholderText("Enter secret code")
        self.secret_code_input.setMinimumSize(100, 40)
        self.secret_code_input.setStyleSheet(
            "font-size: 16px; "
            "border-left: 1px solid 'black'; "
            "border-radius: 0px; "
            "background-color: 'white'; "
            "padding: 0px 10px;"
        )
        icons_dir_path = Path(Path(__file__).parent, "icons")
        layout.addWidget(self.secret_code_input)

        # Clear secret code input field
        self.close = QPushButton()
        self.close.setMinimumSize(40, 40)
        self.close.setIcon(QIcon(str(Path(icons_dir_path, "close.png"))))
        self.close.setIconSize(QSize(20, 20))
        self.close.pressed.connect(lambda: self.secret_code_input.setText(""))
        layout.addWidget(self.close)

        # Button to submit the secret code input
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("font-size: 16px; ")
        submit_button.setMinimumSize(100, 40)
        submit_button.pressed.connect(
            lambda: self._update_secret_code(self.secret_code_input.text())
        )
        layout.addWidget(submit_button)

        return frame

    def _create_filters(self) -> QHBoxLayout:
        """Create and return the filters layout"""
        layout = QHBoxLayout()

        for filter_item in self.level.filters:
            filter_button = QPushButton()
            filter_button.setIcon(QIcon(str(filter_item[0])))
            filter_button.setIconSize(QSize(40, 40))

            filter_idx = self.level.filters.index(filter_item)
            filter_button.pressed.connect(lambda idx=filter_idx: self._change_tab(idx))

            layout.addWidget(filter_button)

        return layout

    def _create_tabbed_controls(self) -> QStackedLayout:
        """Create the tabbed controls layout"""
        layout = QStackedLayout()

        for control_panel in self.filters:
            layout.addWidget(control_panel)

        return layout

    def _change_tab(self, index: int) -> None:
        """
        Change the tabbed controls to the selected index

        :param index:
        :return:
        """
        layout = self._create_tabbed_controls()
        layout.setCurrentIndex(index)

    def update_args_and_image(self, filter_title: str, label: str, value: int, args: dict) -> None:
        """Update the args_cache and then apply the filter with the updated args"""
        # Update the cache with the slider value
        self.args_cache[label] = value

        # Only update args if the keys are present in args_cache
        for key, val in args.items():
            if key in self.args_cache.keys():
                self.args_cache[key] = args[key]

        args_to_pass = self.args_cache
        args_to_pass["second_image"] = args["second_image"]
        args_to_pass["image_to_edit"] = str(self.level.get_image_source())
        args_to_pass["MotionTransformer"] = args["MotionTransformer"]

        new_image = apply_filter(filter_title, args_to_pass)
        self.update_image(new_image)

    def button_pressed_with_two_values(self, filter_title: str, args: dict) -> None:
        """Update the args_cache and then apply the filter with the updated args"""
        # Only update args if the keys are present in args_cache
        for key, val in args.items():
            self.args_cache[key] = args[key]

        args_to_pass = self.args_cache
        args_to_pass["image_to_edit"] = str(self.level.get_image_source())

        new_image = apply_filter(filter_title, args_to_pass)
        self.update_image(new_image)

    def update_image(self, image: QPixmap) -> None:
        """
        Update the image in the main window

        :param image:
        :return:
        """
        self.img_label.setPixmap(image)

    def update_args_cache(self, args: dict) -> None:
        """
        Update the args cache

        :param args:
        :return:
        """
        self.args_cache = args
