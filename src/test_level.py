import sys
import unittest

from PyQt6.QtWidgets import QApplication

from .level import Level


class TestLevel(unittest.TestCase):
    """Tests for level.py"""

    def setUp(self) -> None:
        """Setup QApplication before test cases"""
        self.app = QApplication(sys.argv)

    def test_get_image_source(self) -> None:
        """Test that the right image is received for each level"""
        level_image_source_map = {
            1: 'images/sample.png',
            2: 'images/clockwork.jpg'
        }
        for k, v in level_image_source_map.items():
            test_level = Level(k)
            self.assertEqual(test_level.get_image_source(), v)

    def test_get_image_source_unknown_level(self) -> None:
        """Test that the default image source is chosen on unknown level"""
        test_level = Level(999)
        self.assertEqual(test_level.get_image_source(), 'images/default.png')

    def test_get_secret_answer(self) -> None:
        """Test that the secret answer is correct for each level"""
        secret_answer_map = {
            1: 'secret',
            2: 'secret2'
        }

        for k, v in secret_answer_map.items():
            test_level = Level(k)
            self.assertEqual(test_level.get_secret_answer(), v)

    def test_get_secret_answer_unknown_level(self) -> None:
        """Test that a default string is chosen on unknown level"""
        test_level = Level(999)
        self.assertEqual(test_level.get_secret_answer(), 'pythoncodejam2023')

    # This test literally results in a segfault so I'm gonna wait on that
    # def test_get_filters(self):
    #     print('yeet')
    #     expected_filters_map = {
    #         1: [
    #             (
    #                 'icons/button_sample.png',
    #                 ControlPanel(
    #                     'Image Differencing',
    #                     [('X', (0, 100), Qt.Orientation.Horizontal),
    #                         ('Y', (0, 100), Qt.Orientation.Horizontal)]
    #                 ),
    #             ),
    #             (
    #                 'icons/button_sample2.png',
    #                 ControlPanel(
    #                     'Double Exposure',
    #                     [('Exposure', ('Image 1', 'Image 2'), Qt.Orientation.Horizontal)]
    #                 ),
    #             ),
    #             (
    #                 'icons/button_sample3.png',
    #                 ControlPanel(
    #                     'Motion Manipulation',
    #                     [('Wavelength', (0, 100), Qt.Orientation.Horizontal),
    #                         ('Gap', (0, 100), Qt.Orientation.Horizontal),
    #                         ('Wave Height', (0, 100), Qt.Orientation.Horizontal)]
    #                 ),
    #             )
    #         ],
    #         2: [
    #             (
    #                 'icons/button_sample.png',
    #                 ControlPanel(
    #                     'Image Differencing',
    #                     [('X', (0, 100), Qt.Orientation.Horizontal),
    #                         ('Y', (0, 100), Qt.Orientation.Horizontal)]
    #                 ),
    #             ),
    #             (
    #                 'icons/button_sample2.png',
    #                 ControlPanel(
    #                     'Double Exposure',
    #                     [('Exposure', ('Image 1', 'Image 2'), Qt.Orientation.Horizontal)]
    #                 ),
    #             ),
    #             (
    #                 'icons/button_sample3.png',
    #                 ControlPanel(
    #                     'Motion Manipulation',
    #                     [('Wavelength', (0, 100), Qt.Orientation.Horizontal),
    #                         ('Gap', (0, 100), Qt.Orientation.Horizontal),
    #                         ('Wave Height', (0, 100), Qt.Orientation.Horizontal)]
    #                 ),
    #             )
    #         ]
    #     }
    #     print('yeet')
    #     for k, v in expected_filters_map.items():
    #         test_level = Level(k)
    #         expected_filters = expected_filters_map[k]
    #         self.assertEqual(test_level.get_filters(), expected_filters)

    def test_get_filters_unknown_level(self) -> None:
        """Test that no filter is chosen on unknown level"""
        test_level = Level(level_number=999)

        self.assertEqual(test_level.get_filters(), [])
