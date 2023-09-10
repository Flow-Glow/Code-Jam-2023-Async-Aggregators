from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QFrame, QGridLayout, QHBoxLayout, QLabel, QMainWindow,
    QMessageBox, QStackedLayout, QWidget
)

from src.dock import Dock
from src.level import Level


class Window(QMainWindow):
    """Main Window"""

    def __init__(self, level: Level) -> None:
        super().__init__()
        self.level = level
        self.screen_size = QApplication.primaryScreen().size()
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the User Interface"""
        self.window_name = "Digital Shadows - Async Aggregators"
        self.setWindowTitle(f"{self.window_name} - Level {self.level.level_number}")

        icons_dir_path = Path(Path(__file__).parent, "icons")
        self.setWindowIcon(QIcon(str(Path(icons_dir_path, "logo.png"))))
        layout = self._create_main_layout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _create_main_layout(self) -> QGridLayout:
        """Create the main layout of the application"""
        main_layout = QGridLayout()

        spacer = QLabel()
        main_layout.addWidget(spacer, 0, 0)
        main_layout.addWidget(spacer, 3, 3)

        # Image display
        image_display = self._create_image_display()
        main_layout.addWidget(image_display, 1, 1)

        # Central dock
        self.dock = Dock(self.level, self.img_label, image_display, self._update_secret_code)
        main_layout.addWidget(self.dock, 2, 1)

        return main_layout

    def _create_image_display(self) -> QWidget:
        """Create and return the image display area."""
        frame = QFrame(self)
        frame.setObjectName("image_display_frame")
        frame.setStyleSheet(
            "QFrame#image_display_frame {"
            "border: 1px solid 'black'; "
            "border-radius: 6px; "
            "background-color: '#e4e0e0'; }"
        )

        layout = QHBoxLayout(frame)
        img = QPixmap(str(self.level.img_source))

        # Define max image size constraints (70% of height and 60% of width of the user's primary screen size)
        max_height = self.screen_size.height() * 0.7
        max_width = self.screen_size.width() * 0.6

        # Calculate the scaling factors for width and height
        img_size = img.size()
        width_scale = max_width / img_size.width()
        height_scale = max_height / img_size.height()
        scale_factor = min(width_scale, height_scale)
        qsize = QSize(int(img_size.width() * scale_factor), int(img_size.height() * scale_factor))
        scaled_img = img.scaled(qsize)

        # Convert img_label to an instance variable
        self.img_label = QLabel(self)
        self.img_label.setPixmap(scaled_img)
        self.img_label.setScaledContents(True)  # Removes the discrepancy between true image size and QLabel size

        layout.addWidget(self.img_label)
        layout.addLayout(self._create_tabbed_controls())

        return frame

    def _create_tabbed_controls(self) -> QStackedLayout:
        """Create the tabbed controls layout"""
        layout = QStackedLayout()

        for filter_item in self.level.filters:
            if filter_item[1] is not None:
                layout.addWidget(filter_item[1])

        return layout

    def _update_secret_code(self, input_code: str) -> None:
        """Update the internal secret code and check against the answer."""
        if input_code != self.level.secret_answer:
            # If the input does not match the answer, show a notification
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Error")
            msg_box.setText("\nIncorrect secret code.\n")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.exec()
        else:
            # If the input matches the answer, show a notification
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Success")
            msg_box.setText("\nCorrect secret code.\n")
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.exec()

            self.level = self.level.level_up()
            self._init_ui()
