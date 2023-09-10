import random
from pathlib import Path
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw


def prepare_input(img_path: Path) -> Tuple[Image.Image, List[int]]:
    """
    Prepare the input image by center cropping into a square

    :param img_path: input image file path
    :return: Tuple of cropped input Image and the coordinates of the cropped area
    """
    img = Image.open(img_path)

    # Calculate the square size
    width, height = img.size
    size = min(width, height)

    # Calculate the coordinates for cropping
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2

    # Crop the image to a square
    return img.crop((left, top, right, bottom)), [left, top, right, bottom]


def avg_greyscale(img: Image.Image) -> float:
    """
    Calculates average greyscale or luminance value of an input image

    :param img: input image
    :return: average luminance
    """
    np_img = np.array(img)
    w, h = np_img.shape
    return np.average(np_img.reshape(w * h))


def img_to_ascii(img: Image.Image, dens: int) -> List[str]:
    """
    Given Image and dims (rows, cols) returns an m*n list of Images

    :param img: input image file
    :param dens: greyscale density level
    :return: ascii text generated from input image
    """
    # The amount of text to white space in each of these character determines the greyscale value
    greyscale_strs = [
        "@%#*+=-:. ",  # 10 characters,
        "@%W*hdwOLUzurt|1i}?+>,' ",  # 24 characters,
        "@B$%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1lIi!{}[]?-_+~<>;:,^`'. ",  # 70 characters,
    ]

    # Convert to greyscale (L stands for luminance)
    gs_img = img.convert("L")
    gs_img_w, gs_img_h = gs_img.size[0], gs_img.size[1]
    cols = int(gs_img_w // 10)  # 1/10th of the cropped square
    scale = 0.39  # Aspect ratio of monospace characters

    w = gs_img_w / cols  # tile width
    h = w / scale  # tile height
    rows = int(gs_img_h / h)  # Number of rows of text

    # Generate ascii art
    ascii_ = []
    for r in range(rows):
        y1 = int(r * h)
        y2 = gs_img_h if r == rows - 1 else int((r + 1) * h)
        ascii_.append("")

        for c in range(cols):
            x1 = int(c * w)
            x2 = gs_img_w if c == cols - 1 else int((c + 1) * w)

            # Find average luminance of the cropped tile
            avg = int(avg_greyscale(gs_img.crop((x1, y1, x2, y2))))

            # Find corresponding ascii character by greyscale value and append to the row
            i = int((avg * (len(greyscale_strs[dens]) - 1)) / 255)
            ascii_[r] += greyscale_strs[dens][i]

    return ascii_


def ascii_to_img(
    ascii_text_file_path: Path,
    coordinates: List[int],
    input_img_size: Tuple[int, int],
    output_path: Path,
) -> Image.Image:
    """
    Creates image file from ascii text file

    :param ascii_text_file_path: ascii text file path
    :param coordinates: coordinates used to crop the original image
    :return: Generated image from converting ascii text into PNG
    """
    with open(ascii_text_file_path, "r") as file:
        ascii_text = file.read()
    img_w, img_h = (coordinates[2] - coordinates[0], coordinates[3] - coordinates[1])
    img = Image.new("L", (img_w, img_h), "white")

    # Draw text to image
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox(xy=(0, 0), text=ascii_text)
    left, top, right, bottom = bbox
    w = right - left
    h = bottom - top
    draw.text((0, 0), ascii_text, fill="black")

    # Crop out white spaces and resize to match the original input image size
    output = img.crop((0, 0, w, h)).resize(input_img_size)
    output.save(output_path)
    return output


def seed_secret(ascii_file_path: Path, secret: str, binary_mode: bool) -> None:
    """
    Insert the secret phrase randomly somewhere in the ascii file

    :param ascii_file_path: ascii text file path
    :param secret: secret phrase to hide
    :param binary_mode: whether to hide the text in binary representation
    :return: None
    """
    with open(ascii_file_path, "r") as file:
        lines = file.readlines()

    random_line = random.randint(0, len(lines) - 1)

    # Convert to binary representation if chosen 'insane mode'
    if binary_mode:
        secret = "".join(map(bin, bytearray(secret, "utf8")))

    line_length = len(lines[random_line])
    secret_length = len(secret)

    position = random.randint(0, line_length - secret_length - 1)
    lines[random_line] = "".join(
        [
            lines[random_line][0:position],
            secret,
            lines[random_line][position + secret_length :],
        ]
    )

    with open(ascii_file_path, "w") as file:
        file.writelines(lines)


def validate_image_size(input_img: Image.Image) -> None:
    """
    For the quality of the tool, the image must be larger than 1000x1000

    :param input_img: Prepared input PIL Image
    :return: None
    """
    input_img_w, input_img_h = input_img.size
    if input_img_w < 1000 or input_img_h < 1000:
        raise ValueError("Please provide an image size bigger than 1000x1000!")


def validate_secret_length(secret: str, input_img_w: int) -> None:
    """
    The secret phrase cannot be too long otherwise the puzzle will be too obvious

    :param secret: Secret phrase
    :param input_img_w: Width of the input image
    :return: None
    """
    if len(secret) > input_img_w // 100:
        raise ValueError(
            "The secret phrase provided is too long to be hidden in this image size."
        )


def generate_ascii_file(
    input_img: Image.Image, ascii_file_path: Path, dens: int
) -> None:
    """
    Generate ascii file from image input

    :param input_img: PIL prepared input image
    :param ascii_file_path: Destination location of the ascii output
    :param dens: Quality of the greyscale between range of 0,1,2
    :return: None
    """
    with open(ascii_file_path, "w") as f:
        for row in img_to_ascii(input_img, dens):
            f.write(row + "\n")
