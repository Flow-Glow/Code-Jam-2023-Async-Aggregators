from PIL import Image


def double_exposure(img1: Image, img2: Image, alpha: float = 0.5) -> Image:
    """
    Blend two images together using alpha blending

    :param img1: PIL Image
    :param img2: PIL Image
    :param alpha: int
    :return:
    """
    # Ensure img1 is the smaller image, or swap if necessary
    if img1.size[0] > img2.size[0] or img1.size[1] > img2.size[1]:
        img1, img2 = img2, img1

    # Convert both images to RGB
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # Resize img2 to match img1's size
    img2 = img2.resize(img1.size)

    # Blend the images
    blended = Image.blend(img2, img1, alpha)

    return blended
