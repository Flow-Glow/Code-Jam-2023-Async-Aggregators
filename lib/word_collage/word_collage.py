import argparse
from typing import List

import numpy as np
from PIL import Image, ImageDraw


def avg_greyscale(img: Image.Image) -> None:
    """
    Calculates average greyscale or luminance value of an input image

    :param img: input image
    :return: average luminance
    """
    np_img = np.array(img)
    w, h = np_img.shape
    return np.average(np_img.reshape(w * h))


def img_to_ascii(img: Image.Image, cols: int, scale: float, dens: int) -> None:
    """
    Given Image and dims (rows, cols) returns an m*n list of Images

    :param img: input image file
    :param cols: number of columns
    :param scale: aspect ratio scale
    :param dens: greyscale density level
    :return: ascii text generated from input image
    """
    # The amount of text to white space in each of these character determines the greyscale value
    greyscale_strs = [
        "@%#*+=-:. ",  # 10 characters,
        "@%W*hdwOLUzurt|1i}?+>,' ",  # 24 characters,
        "@B$%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1lIi!{}[]?-_+~<>;:,^`'. "  # 70 characters,
    ]

    gs_img = Image.open(img).convert("L")  # Convert to grayscale (L stands for luminance)
    gs_img_w, gs_img_h = gs_img.size[0], gs_img.size[1]

    w = gs_img_w / cols  # Output width
    h = w / scale  # Output height
    rows = int(gs_img_h / h)  # Number of rows of text

    print(f"Original image size: {gs_img_w} x {gs_img_h}")
    print(f"Output ascii size: {w} x {h}")
    print(f"Output cols & rows: {cols} x {rows}")

    # Input image size validation
    if gs_img_w < cols or gs_img_h < rows:
        raise ValueError("Image not big enough for specified number of columns.")

    # Generate ascii art
    ascii_ = []
    for r in range(rows):
        y1 = int(r * h)
        y2 = gs_img_h if r == rows - 1 else int((r + 1) * h)
        ascii_.append("")

        for c in range(cols):
            x1 = int(c * w)
            x2 = gs_img_w if c == cols - 1 else int((c + 1) * w)

            avg = int(avg_greyscale(gs_img.crop((x1, y1, x2, y2))))  # Find average luminance

            # Find corresponding ascii character by greyscale value and append to the row
            ascii_[r] += greyscale_strs[dens][int((avg * (len(greyscale_strs[dens]) - 1)) / 255)]

    return ascii_


def ascii_to_img() -> None:
    """
    Creates image file from ascii text file

    :return: generated ascii image
    """
    with open("result.txt", "r") as file:
        ascii_text = file.read()

    img_w, img_h = (750, 750)
    im = Image.new("RGBA", (img_w, img_h), "white")

    # Draw text to image
    draw = ImageDraw.Draw(im)
    bbox = draw.textbbox(xy=(0, 0), text=ascii_text)
    left, top, right, bottom = bbox
    w = right - left
    h = bottom - top

    # Center the drawing
    draw.text(((img_w - w) / 2, (img_h - h) / 2), ascii_text, fill="black")

    im.save("result.png", "png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", dest="img", required=True)
    parser.add_argument("--scale", dest="scale", required=False, default=0.5)
    parser.add_argument("--cols", dest="cols", required=False, default=100)
    parser.add_argument("--dens", dest="dens", required=False, default=2)
    args = parser.parse_args()

    with open("result.txt", "w") as f:
        for row in img_to_ascii(args.img, int(args.cols), float(args.scale), int(args.dens)):
            f.write(row + "\n")

    ascii_to_img()