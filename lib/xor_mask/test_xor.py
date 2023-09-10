import shutil
import unittest
from pathlib import Path
from typing import Any

from .xor_mask import generate_image, generate_xor_pair, mask_images


class TestXorMask(unittest.TestCase):
    """
    Test cases for XOR masking

    Test generating alphanumeric character to image
    Test separating char image into two different XOR pair images
    Test that the two pairs can generate the original image when masked together
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize inputs"""
        super().__init__(*args, **kwargs)
        self.secret = "PYTHON"
        self.base_xor_image_path = Path("images/xor_mask/")

    def setUp(self) -> None:
        """Prepare the original images based on the characters in secret"""
        self.original_images = {}
        for c in self.secret:
            self.original_images[c] = generate_image(c, 2)

    def test_generate_image_medium_difficulty(self) -> None:
        """Test that the characters in the secret word is generated into image of correct size"""
        self.assertEqual(len(self.original_images), len(self.secret))
        self.assertEqual(
            self.original_images[next(iter(self.original_images))].size, (50, 50)
        )

    def test_generate_xor_mask_pair_images(self) -> None:
        """Test that the original image creates two xor pair images"""
        for c in self.original_images:
            img1, img2 = generate_xor_pair(self.original_images[c], c)
            self.assertEqual(img1.size, img2.size)
            self.assertEqual(self.original_images[c].size, img1.size)
            masked = mask_images(img1, img2)
            self.assertEqual(masked.tobytes(), self.original_images[c].tobytes())

    def tearDown(self) -> None:
        """Clean up output directory"""
        if self.base_xor_image_path.exists():
            shutil.rmtree(self.base_xor_image_path)
