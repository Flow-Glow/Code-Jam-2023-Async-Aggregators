import unittest
from pathlib import Path
from typing import Any

from PIL import Image

from .hidden_in_ascii import (
    ascii_to_img, generate_ascii_file, img_to_ascii, prepare_input,
    seed_secret, validate_image_size, validate_secret_length
)


def string_exists_in_file(file_path: Path, target_string: str) -> bool:
    """
    Checks if given string exists in the file

    :param file_path: Path to the file
    :param target_string: search string
    :return: True if the search string exists in the file
    """
    try:
        with open(file_path, "r") as file:
            file_contents = file.read()
            return target_string in file_contents
    except FileNotFoundError:
        return False


class TestPrepareInputImage(unittest.TestCase):
    """Test cases for preparing input image"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize inputs"""
        super().__init__(*args, **kwargs)
        self.input_file_path = Path("src/images/doggo.jpg")

    def test_input_file_exists(self) -> None:
        """Check that the test file that will be used in this test suite exists in the directory"""
        self.assertTrue(
            self.input_file_path.exists(),
            f"Test file '{self.input_file_path}' does not exist",
        )

    def test_validate_image_size_exception(self) -> None:
        """Test that image validation raises errors on invalid image size"""
        input_image = Image.open(self.input_file_path)
        small_image = input_image.crop((0, 0, 100, 100))
        with self.assertRaises(ValueError) as e:
            validate_image_size(small_image)
        self.assertEqual(
            str(e.exception), "Please provide an image size bigger than 1000x1000!"
        )

    def test_validate_secret_length_exception(self) -> None:
        """Test that validation raises errors if the secret phrase is too long compared to image size"""
        input_image_w = 1000
        secret = "a" * 11
        with self.assertRaises(ValueError) as e:
            validate_secret_length(secret, input_image_w)
        self.assertEqual(
            str(e.exception),
            "The secret phrase provided is too long to be hidden in this image size.",
        )

    def test_prepare_input(self) -> None:
        """Test that input is properly cropped to a square"""
        input_img, coordinates = prepare_input(self.input_file_path)

        # Assert that the image is cropped to a square
        w, h = input_img.size
        self.assertEqual(w, h)

        # Assert that the cropped size is same as the calculated coordinates
        # coordinate -> [left, top, right, bottom]
        self.assertEqual(w, coordinates[2] - coordinates[0])
        self.assertEqual(h, coordinates[3] - coordinates[1])


class TestImageToAscii(unittest.TestCase):
    """Test cases for converting image to ascii text file"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize inputs"""
        super().__init__(*args, **kwargs)
        self.input_file_path = Path("src/images/doggo.jpg")
        self.dens = 2

    def setUp(self) -> None:
        """Prepare input image"""
        self.input_img, self.coordinates = prepare_input(self.input_file_path)

    def test_img_to_ascii(self) -> None:
        """Test that image has converted to proper amount of ascii text"""
        ascii_list = img_to_ascii(self.input_img, self.dens)
        input_img_w, input_img_h = self.input_img.size
        cols = int(input_img_w // 10)
        scale = 0.39
        w = input_img_w / cols
        h = w / scale

        # Assert the number of rows returned is same as expected
        self.assertEqual(len(ascii_list), int(input_img_h / h))

        # Assert the number of cols in each row is same as expected
        self.assertEqual(len(ascii_list[0]), cols)


class TestAsciiToImage(unittest.TestCase):
    """Test cases for converting ascii text file back to output image"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize inputs"""
        super().__init__(*args, **kwargs)
        self.input_file_path = Path("src/images/doggo.jpg")
        self.output_file_path = Path("src/images/output.png")
        self.dens = 2
        self.insane_mode = False
        self.ascii_file_path = Path("lib/hidden_in_ascii/ascii.txt")
        self.secret = "Very secret"

    def setUp(self) -> None:
        """Prepare input image and generate ascii text file"""
        self.input_img, self.coordinates = prepare_input(self.input_file_path)
        generate_ascii_file(self.input_img, self.ascii_file_path, self.dens)

    def test_ascii_file(self) -> None:
        """Test that the secret phrase is hidden in the ascii text file"""
        self.assertTrue(self.ascii_file_path.exists())
        seed_secret(self.ascii_file_path, self.secret, self.insane_mode)
        self.assertTrue(string_exists_in_file(self.ascii_file_path, self.secret))

    def test_ascii_to_image(self) -> None:
        """Test that the output file has been created and that the image size is appropriate"""
        output_img = ascii_to_img(
            self.ascii_file_path,
            self.coordinates,
            self.input_img.size,
            self.output_file_path,
        )
        self.assertTrue(self.output_file_path.exists())
        self.assertEqual(output_img.size, self.input_img.size)

    def tearDown(self) -> None:
        """Clean up output files"""
        if self.ascii_file_path.exists():
            self.ascii_file_path.unlink()

        if self.output_file_path.exists():
            self.output_file_path.unlink()
