from PyQt6.QtCore import Qt

import control_panel


class Level:
    """Class to represent a level in the game/application."""

    def __init__(self, level_number: int):
        self.level_number = level_number
        self.secret_answer = self.get_secret_answer()
        self.img_source = self.get_image_source()
        self.filters = self.get_filters()

    def get_image_source(self) -> str:
        """
        Get the image source for the level

        :return: str
        """
        # This can be extended to retrieve images dynamically based on the level
        if self.level_number == 1:
            return 'images/sample.png'
        if self.level_number == 2:
            return 'images/clockwork.jpg'
        return 'images/default.png'

    def get_secret_answer(self) -> str:
        """
        Get the secret answer for the level

        :return: str
        """
        # This can be extended to provide answers dynamically based on the level
        if self.level_number == 1:
            return 'secret'
        if self.level_number == 2:
            return 'secret2'
        return 'pythoncodejam2023'

    def get_filters(self) -> list:
        """
        Get the filters for the level

        :return: list
        """
        # This can be extended to provide filters dynamically based on the level
        if self.level_number == 1:
            filters = [
                (
                    'icons/button_sample.png',
                    control_panel.ControlPanel(
                        'Image Differencing',
                        [('X', (0, 100), Qt.Orientation.Horizontal),
                         ('Y', (0, 100), Qt.Orientation.Horizontal)]
                    ),
                ),
                (
                    'icons/button_sample2.png',
                    control_panel.ControlPanel(
                        'Double Exposure',
                        [('Exposure', ('Image 1', 'Image 2'), Qt.Orientation.Horizontal)]
                    ),
                ),
                (
                    'icons/button_sample3.png',
                    control_panel.ControlPanel(
                        'Motion Manipulation',
                        [('Wavelength', (0, 100), Qt.Orientation.Horizontal),
                         ('Gap', (0, 100), Qt.Orientation.Horizontal),
                         ('Wave Height', (0, 100), Qt.Orientation.Horizontal)]
                    ),
                )
            ]
            return filters
        if self.level_number == 2:
            return [
                (
                    'icons/button_sample.png',
                    control_panel.ControlPanel(
                        'Image Differencing',
                        [
                            ('X', (0, 100), Qt.Orientation.Horizontal),
                            ('Y', (0, 100), Qt.Orientation.Horizontal)
                        ]
                    ),
                ),
                (
                    'icons/button_sample2.png',
                    control_panel.ControlPanel(
                        'Double Exposure',
                        [('Exposure', ('Image 1', 'Image 2'), Qt.Orientation.Horizontal)]
                    ),
                ),
                (
                    'icons/button_sample3.png',
                    control_panel.ControlPanel(
                        'Motion Manipulation',
                        [
                            ('Wavelength', (0, 100), Qt.Orientation.Horizontal),
                            ('Gap', (0, 100), Qt.Orientation.Horizontal),
                            ('Wave Height', (0, 100), Qt.Orientation.Horizontal)
                        ]
                    ),
                )
            ]

        return []
