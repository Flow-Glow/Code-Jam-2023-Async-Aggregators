from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QStackedLayout, QWidget
)

from level import Level


class Window(QMainWindow):
    """Main Window"""

    def __init__(self, level: Level) -> None:
        super().__init__()
        self.secret_answer = level.secret_answer
        self.level = level
        self.secret_code = ""
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the User Interface"""
        self.window_name = 'Digital Shadows - Async Aggregators'
        self.setWindowTitle(f"{self.window_name} - Level {self.level.level_number}")
        layout = self._create_main_layout()

        widget = QWidget()
        widget.setLayout(layout)
        widget.setMinimumSize(850, 450)
        widget.setMaximumHeight(450)
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
        central_dock = self._create_central_dock()
        main_layout.addLayout(central_dock, 2, 1)

        return main_layout

    def _create_image_display(self) -> QWidget:
        """Create and return the image display area."""
        frame = QFrame(self)
        frame.setObjectName("image_display_frame")
        frame.setStyleSheet('QFrame#image_display_frame {'
                            'border: 1px solid "black"; '
                            'border-radius: 6px; '
                            'background-color: "#e4e0e0"; }')

        layout = QHBoxLayout(frame)
        img = QPixmap(self.level.img_source).scaled(450, 450, Qt.AspectRatioMode.KeepAspectRatio)
        img_label = QLabel(self)
        img_label.setPixmap(img)

        layout.addWidget(img_label)
        layout.addLayout(self._create_tabbed_controls())

        return frame

    def _create_tabbed_controls(self) -> QStackedLayout:
        """Create the tabbed controls layout"""
        layout = QStackedLayout()

        for filter_item in self.level.filters:
            layout.addWidget(filter_item[1])

        return layout

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
        frame.setStyleSheet('QFrame#filter_dock_frame {'
                            'border: 1px solid "black";'
                            'border-radius: 6px; '
                            'background-color: "white";}')
        layout = QHBoxLayout(frame)

        # Filters
        filters = self._create_filters()
        layout.addLayout(filters)

        # Secret code input field
        self.secret_code_input = QLineEdit()
        self.secret_code_input.setPlaceholderText("Enter secret code")
        self.secret_code_input.setMinimumSize(100, 40)
        self.secret_code_input.setStyleSheet('font-size: 16px; '
                                             'border-left: 1px solid "black"; '
                                             'border-radius: 0px; '
                                             'background-color: "white"; '
                                             'padding: 0px 10px;')

        layout.addWidget(self.secret_code_input)

        # Clear secret code input field
        self.close = QPushButton()
        self.close.setMinimumSize(40, 40)
        self.close.setIcon(QIcon('icons\\close.png'))
        self.close.setIconSize(QSize(20, 20))
        self.close.pressed.connect(lambda: self.secret_code_input.setText(''))
        layout.addWidget(self.close)

        # Button to submit the secret code input
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet('font-size: 16px; ')
        submit_button.setMinimumSize(100, 40)
        submit_button.pressed.connect(lambda: self._update_secret_code(self.secret_code_input.text()))
        layout.addWidget(submit_button)

        return frame

    def _create_filters(self) -> QHBoxLayout:
        """Create and return the filters layout"""
        layout = QHBoxLayout()

        for filter_item in self.level.filters:
            filter_button = QPushButton()
            filter_button.setIcon(QIcon(filter_item[0]))
            filter_button.setIconSize(QSize(40, 40))

            filter_idx = self.level.filters.index(filter_item)
            filter_button.pressed.connect(lambda idx=filter_idx: self._change_tab(idx))

            layout.addWidget(filter_button)

        return layout

    def _change_tab(self, index: int) -> None:
        """Change the current index of the tabbed controls layout"""
        layout = self._create_tabbed_controls()
        layout.setCurrentIndex(index)

    def _update_secret_code(self, input_code: str) -> None:
        """Update the internal secret code and check against the answer."""
        self.secret_code = input_code

        if self.secret_code != self.secret_answer:
            # If the input does not match the answer, show a notification
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Error')
            msg_box.setText('Incorrect secret code.')
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.exec()
        else:
            # If the input matches the answer, show a notification
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Success')
            msg_box.setText('Correct secret code.')
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.exec()

            self.level.level_number += 1
            self.setWindowTitle(f'{self.window_name} - Level {self.level.level_number}')
