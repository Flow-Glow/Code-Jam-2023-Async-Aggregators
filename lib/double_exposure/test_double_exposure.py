import unittest

from PIL import Image

from .double_exposure import double_exposure


class DoubleExposureTestCase(unittest.TestCase):
    """Tests For double_exposure.py"""

    def test_alpha_half(self) -> None:
        """
        Test that blending with default alpha=0.5 results in a blend of two images and preserves image size.

        :return: None
        """
        # Load two example images
        image1 = Image.new("RGB", (200, 200), (0, 255, 0))
        image2 = Image.new("RGB", (200, 200), (255, 0, 0))

        # Call the double_exposure function
        result_image = double_exposure(image2, image1)

        # Check if the size of the result image matches the input images
        self.assertEqual(result_image.size, (200, 200))

        # Check if the result image matches a blend of the two images
        expected_image = Image.new("RGB", (200, 200), (127, 127, 0))
        self.assertEqual(result_image, expected_image)

    def test_alpha_zero(self) -> None:
        """
        Test that blending with alpha=0.0 results in the first image unchanged and preserves image size.

        :return: None
        """
        # Create two images with different colors
        image1 = Image.new("RGB", (200, 200), (255, 0, 0))  # Red
        image2 = Image.new("RGB", (200, 200), (0, 255, 0))  # Green

        # Blend the images with alpha = 0.0 (result should be the first image)
        result_image = double_exposure(image2, image1, alpha=0.0)

        # Check if the size of the result image matches the input images
        self.assertEqual(result_image.size, (200, 200))

        # Check if the result image matches the first image
        self.assertEqual(result_image, image1)

    def test_alpha_one(self) -> None:
        """
        Test that blending with alpha=1.0 results in the second image unchanged and preserves image size.

        :return: None
        """
        # Create two images with different colors
        image1 = Image.new("RGB", (200, 200), (255, 0, 0))  # Red
        image2 = Image.new("RGB", (200, 200), (0, 255, 0))  # Green

        # Blend the images with alpha = 1.0 (result should be the second image)
        result_image = double_exposure(image2, image1, alpha=1.0)

        # Check if the size of the result image matches the input images
        self.assertEqual(result_image.size, (200, 200))

        # Check if the result image matches the second image
        self.assertEqual(result_image, image2)
