from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def generate_image(alphanumeric: str, difficulty: int) -> Image.Image:
    """
    Generate an image of the character

    :param alphanumeric: alphanumeric character
    :param difficulty: difficulty level ranging from 1-3
    :return: Generated PIL image
    """
    difficulty_properties = {
        1: {"image_size": (12, 12), "font_size": 14, "offset": (3, -2)},
        2: {"image_size": (50, 50), "font_size": 64, "offset": (8, -10)},
        3: {"image_size": (100, 100), "font_size": 130, "offset": (20, -20)},
    }

    # Get the image properties based on the difficulty level, default to level 3
    properties = difficulty_properties.get(difficulty, difficulty_properties[3])

    image_size = properties["image_size"]
    font_size = properties["font_size"]
    offset = properties["offset"]

    image = Image.new("L", image_size, "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        str(Path("lib/xor_mask/BebasNeue-Regular.ttf")), font_size
    )
    # Draw the character in black on the image
    draw.text(offset, alphanumeric, fill="black", font=font, spacing=0)
    binary_image = image.point(lambda p: 255 if p > 128 else 0)
    output_directory = Path("images/xor_mask")
    output_directory.mkdir(parents=True, exist_ok=True)
    binary_image.save(Path(f"images/xor_mask/{alphanumeric}.png"))
    return binary_image


def generate_xor_pair(
    image: Image.Image, alphanumeric: str
) -> tuple[Image.Image, Image.Image]:
    """
    Split the original image into two images suc that when XORed, can reconstruct the original image back

    :param image: greyscale image
    :param alphanumeric: character that is represented in the image
    :return: Tuple pair of generated two images that can rebulid original image when XORed
    """
    # Create two blank images with the same size
    image1 = Image.new("L", image.size)
    image2 = Image.new("L", image.size)

    # Convert images to numpy arrays for manipulation
    original_array = np.array(image)
    image1_array = np.array(image1)
    image2_array = np.array(image2)

    # Split the original image into two XOR pair images
    for i in range(original_array.shape[0]):
        for j in range(original_array.shape[1]):
            """
            A | B | A XOR B
            ----------------
            0 | 0 | 0
            1 | 0 | 1
            0 | 1 | 1
            1 | 1 | 0
            """
            if original_array[i][j] >= 128:
                # If the original pixel is white randomly choose the two images to either have black or white pixel
                if np.random.randint(2) == 0:
                    image1_array[i][j] = 255
                    image2_array[i][j] = 255
                else:
                    image1_array[i][j] = 0
                    image2_array[i][j] = 0
            else:
                # If the original pixel is black, randomly choose one of the image to be black pixel
                # and the other image to be white pixel
                if np.random.randint(2) == 0:
                    image1_array[i][j] = 0
                    image2_array[i][j] = 255
                else:
                    image1_array[i][j] = 255
                    image2_array[i][j] = 0

    # Convert numpy arrays back to images
    image1 = Image.fromarray(image1_array)
    image2 = Image.fromarray(image2_array)

    # Save the two new images
    output_directory = Path("images/xor_mask")
    output_directory.mkdir(parents=True, exist_ok=True)
    image1.save(Path(f"images/xor_mask/{alphanumeric}_1.png"))
    image2.save(f"images/xor_mask/{alphanumeric}_2.png")
    return image1, image2


def mask_images(image1: Image.Image, image2: Image.Image) -> Image.Image:
    """
    Mask two input image to generate a new image

    :param image1: First PIL image
    :param image2: Second PIL image
    :return: Masked PIL image
    """
    w, h = image1.size
    # Create blank result image
    result = Image.new("L", (w, h))

    # Convert images to numpy arrays for manipulation
    image1_array = np.array(image1)
    image2_array = np.array(image2)
    result_array = np.array(result)

    # XOR all the pixels from both images to generate the masked image
    for i in range(w):
        for j in range(h):
            result_array[i][j] = (
                255 if image1_array[i][j] ^ image2_array[i][j] == 0 else 0
            )

    # Convert numpy arrays back to images
    result = Image.fromarray(result_array)
    return result
