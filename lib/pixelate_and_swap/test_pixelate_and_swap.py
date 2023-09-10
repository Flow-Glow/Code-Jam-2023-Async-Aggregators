import unittest
from pathlib import Path

from PIL import Image

from .pixelate_and_swap import pixelate_and_group_colors_sampled, swap_colors


class TestPixelate(unittest.TestCase):
    """Test cases for pixelate_and_swap.py"""

    def test_pixelate_and_group_colors_sampled(self) -> None:
        """
        Test that the number of colors in an image after pixelation is less than the number of colors before pixelation

        :return: None
        """
        # Get the directory of the current script using pathlib.
        script_dir = Path(__file__).parent

        # Construct a relative path to the image file using pathlib.
        image_path = script_dir / "dahlias.jpg"

        image = Image.open(image_path)

        # Count the number of colors in the image before pixelation
        colors_before = len(set(image.getdata()))

        # Pixelate and group colors
        pixelated = pixelate_and_group_colors_sampled(image, 8)

        # Count the number of colors in the image after pixelation
        colors_after = len(set(pixelated.getdata()))

        # Assert that the number of colors after pixelation is less than the number of colors before pixelation
        self.assertLess(colors_after, colors_before)

        assert colors_before > colors_after
        assert colors_before != colors_after
        assert colors_after == 8


class TestSwap(unittest.TestCase):
    """Test cases for pixelate_and_swap.py"""

    def test_swap_colors(self) -> None:
        """
        Test that the number of white pixels after swapping is equal to the number of black pixels before swapping

        :return: None
        """
        # Create a test image
        test_image = Image.new("RGB", (100, 100), "white")

        # Count the number of white and black pixels in the image
        white_pixels_before_swap = 0
        black_pixels_before_swap = 0
        for pixel in test_image.getdata():
            if pixel == (255, 255, 255):
                white_pixels_before_swap += 1
            elif pixel == (0, 0, 0):
                black_pixels_before_swap += 1

        # Swap white and black colors
        swapped = swap_colors(test_image, (255, 255, 255), (0, 0, 0))

        # Count the number of white and black pixels in the image
        white_pixels_after_swap = 0
        black_pixels_after_swap = 0
        for pixel in swapped.getdata():
            if pixel == (255, 255, 255):
                white_pixels_after_swap += 1
            elif pixel == (0, 0, 0):
                black_pixels_after_swap += 1

        # Assert that the number of white pixels after swapping is equal to the number of black pixels before swapping
        self.assertEqual(white_pixels_after_swap, black_pixels_before_swap)

        # Assert that the number of black pixels after swapping is equal to the number of white pixels before swapping
        self.assertEqual(black_pixels_after_swap, white_pixels_before_swap)

        # Assert that there are no other colors in the image
        for pixel in swapped.getdata():
            self.assertIn(pixel, [(255, 255, 255), (0, 0, 0)])

    def test_swap_three_colors(self) -> None:
        """Swap two colors in an image and verify third color is unchanged

        Test that after swapping, the number of white pixels is equal to the initial number of black pixels, the number
        of black pixels is equal to the initial number of white pixels,and the number of red pixels remains unchanged
        :return: None
        """
        # Create a test image with three colors
        test_image = Image.new("RGB", (100, 100))
        for i in range(100):
            for j in range(100):
                if i < 33:
                    test_image.putpixel((i, j), (255, 255, 255))  # White
                elif 33 <= i < 66:
                    test_image.putpixel((i, j), (0, 0, 0))  # Black
                else:
                    test_image.putpixel((i, j), (255, 0, 0))  # Red

        # Count the number of white, black, and red pixels in the image
        colors_before_swap = {
            (255, 255, 255): 0,  # White
            (0, 0, 0): 0,  # Black
            (255, 0, 0): 0,  # Red
        }
        for pixel in test_image.getdata():
            if pixel in colors_before_swap:
                colors_before_swap[pixel] += 1

        # Swap white and black colors
        swapped = swap_colors(test_image, (255, 255, 255), (0, 0, 0))

        # Count the number of white, black, and red pixels in the swapped image
        colors_after_swap = {
            (255, 255, 255): 0,  # White
            (0, 0, 0): 0,  # Black
            (255, 0, 0): 0,  # Red
        }
        for pixel in swapped.getdata():
            if pixel in colors_after_swap:
                colors_after_swap[pixel] += 1

        # Assert that the number of white pixels after swapping is equal to the number of black pixels before swapping
        self.assertEqual(
            colors_after_swap[(255, 255, 255)], colors_before_swap[(0, 0, 0)]
        )

        # Assert that the number of black pixels after swapping is equal to the number of white pixels before swapping
        self.assertEqual(
            colors_after_swap[(0, 0, 0)], colors_before_swap[(255, 255, 255)]
        )

        # Assert that the number of red pixels remains unchanged
        self.assertEqual(
            colors_after_swap[(255, 0, 0)], colors_before_swap[(255, 0, 0)]
        )

        # Assert that there are no other colors in the swapped image
        for pixel in swapped.getdata():
            self.assertIn(pixel, [(255, 255, 255), (0, 0, 0), (255, 0, 0)])
