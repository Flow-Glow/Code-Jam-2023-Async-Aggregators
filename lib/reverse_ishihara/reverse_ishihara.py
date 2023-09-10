import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from src.utils.lru_cache_pil import LRUCachePIL

# Global cache object with, for example, a capacity of 10 images
image_cache = LRUCachePIL(10)


def reverse_ishihara(
    image: Image.Image,
    message: str = None,
    color_blind_color: tuple = (155, 155, 0),
    noise_color: tuple = (150, 151, 0),
    noise_density: float = 0.006,
    dot_radius: int = 6,
) -> Image.Image:
    """
    Generate a reverse Ishihara image from an input image.

    :param image: PIL Image object
    :param message: Optional message or number to display using dots
    :param color_blind_color: Color for the message, distinguishable by color-blind individuals
    :param noise_color: Color for noise, not distinguishable by non-color blind individuals from the message color
    :param noise_density: Density of the noise in the image (0 to 1)
    :param dot_radius: Radius of the noise dots
    :return: PIL Image object
    """
    draw = ImageDraw.Draw(image)

    # Draw the message using dots if provided
    if message:
        font_path = "MontserratRegular-BWBEl.ttf"  # Point to a TTF or OTF font file on your machine
        font = ImageFont.truetype(font_path, int(image.height * 0.5))

        left, top, right, bottom = font.getbbox(message)
        text_width, text_height = right - left, bottom - top

        text_img = Image.new("1", (text_width, text_height), color="white")
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text(
            (-left, -top), message, fill="black", font=font
        )  # Notice the negative offsets

        dot_density_for_text = (
            0.001  # This determines the density of the dots. Adjust as needed (0 to 1).
        )

        center_x_offset = (image.width - text_width) // 2
        center_y_offset = (image.height - text_height) // 2

        # For each black pixel in the text image, draw a dot on the main image
        for y in range(text_height):
            for x in range(text_width):
                if (
                    text_img.getpixel((x, y)) == 0
                    and random.random() < dot_density_for_text
                ):
                    # Adjust these lines to position the text at the center
                    center_x = x + center_x_offset
                    center_y = y + center_y_offset
                    draw.ellipse(
                        [
                            (center_x - dot_radius, center_y - dot_radius),
                            (center_x + dot_radius, center_y + dot_radius),
                        ],
                        fill=color_blind_color,
                    )

    # Add noise
    num_noise_dots = int(noise_density * image.width * image.height)
    for _ in range(num_noise_dots):
        x = random.randint(0 + dot_radius, image.width - 1 - dot_radius)
        y = random.randint(0 + dot_radius, image.height - 1 - dot_radius)
        draw.ellipse(
            [(x - dot_radius, y - dot_radius), (x + dot_radius, y + dot_radius)],
            fill=noise_color,
        )

    return image


def unmask_reverse_ishihara(
    image_path: str, a_scale: int = 2, b_scale: int = 2
) -> np.array:
    """
    Unmask a reverse Ishihara image

    :param image_path:
    :param a_scale:
    :param b_scale:
    :return:
    """
    image = cv2.imread(image_path)
    if image is None:
        print("Error reading the image.")
        return None

    # Convert to LAB
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Scale the 'a' and 'b' channels
    a_channel = cv2.normalize(a_channel * a_scale, None, 0, 255, cv2.NORM_MINMAX)
    b_channel = cv2.normalize(b_channel * b_scale, None, 0, 255, cv2.NORM_MINMAX)

    # Merge the channels back
    enhanced_lab_image = cv2.merge(
        [l_channel, a_channel.astype(np.uint8), b_channel.astype(np.uint8)]
    )

    # Convert back to RGB
    enhanced_rgb_image = cv2.cvtColor(enhanced_lab_image, cv2.COLOR_Lab2BGR)

    # Considering the blue channel might have the difference we need (as before), threshold it
    _, b_channel = cv2.threshold(enhanced_rgb_image[:, :, 2], 1, 255, cv2.THRESH_BINARY)

    # Erode to enhance the message dots over the noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(b_channel, kernel, iterations=1)

    # Extract message
    result = cv2.bitwise_and(enhanced_rgb_image, enhanced_rgb_image, mask=mask)

    # cv2.imwrite("enhanced.png", result)

    return result
