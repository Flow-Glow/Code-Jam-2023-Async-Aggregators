import math
from enum import Enum, auto
from typing import List

import numpy as np
from PIL import Image


class PIXEL_INTERPOLATION_METHOD(Enum):
    INTEGER = auto()


class OFF_CANVAS_FILL(Enum):
    WRAP = auto()
    MIRROR = auto()
    EDGE = auto()


class Effect:
    @staticmethod
    def explode(xmesh, ymesh, magnitude=1):
        height, width = xmesh.shape
        normalized_distance = (
            (xmesh / width - 0.5) ** 2 + (ymesh / height - 0.5) ** 2
        ) ** 0.5
        new_distance = normalized_distance / (
            np.maximum((1 - normalized_distance) * 3 * magnitude, 1) + 0.1
        )
        xmesh = (xmesh - width / 2) * new_distance / normalized_distance + width / 2
        ymesh = (ymesh - height / 2) * new_distance / normalized_distance + height / 2
        return xmesh, ymesh

    @staticmethod
    def vertical_wave(xmesh, ymesh, wavenum=1.5, magnitude=1):
        height, width = xmesh.shape
        offset = np.sin(xmesh / width * math.pi * 2 * wavenum) * magnitude * height / 4
        return xmesh, ymesh + offset

    @staticmethod
    def horizontal_wave(xmesh, ymesh, wavenum=1.5, magnitude=1):
        height, width = xmesh.shape
        offset = np.sin(ymesh / height * math.pi * 2 * wavenum) * magnitude * width / 4
        return xmesh + offset, ymesh

    @staticmethod
    def vertical_spike(xmesh, ymesh, spikenum=5, magnitude=1):
        _, width = xmesh.shape
        spike_distance = width // spikenum
        offset = np.abs(xmesh % spike_distance - spike_distance // 2) * magnitude * 2
        return xmesh, ymesh + offset

    @staticmethod
    def horizontal_spike(xmesh, ymesh, spikenum=5, magnitude=1):
        height, _ = xmesh.shape
        spike_distance = height // spikenum
        offset = np.abs(ymesh % spike_distance - spike_distance // 2) * magnitude * 2
        return xmesh + offset, ymesh


class Motion_Transformer:
    def __init__(
        self,
        img: Image.Image,
        interpolation: PIXEL_INTERPOLATION_METHOD = PIXEL_INTERPOLATION_METHOD.INTEGER,
        fill_method: OFF_CANVAS_FILL = OFF_CANVAS_FILL.MIRROR,
        funclist=(
            Effect.horizontal_wave,
            Effect.horizontal_spike,
            Effect.vertical_wave,
        ),
    ):
        self.img = img
        self.interpolation = interpolation
        self.fill_method = fill_method
        self.funclist = funclist
        self._generate_mesh()

    def reset_cache(self):
        self.cache = {}

    def update_image(self, img):
        if img.shape != self.img.shape:
            self._generate_mesh()
        self.img = img

    def calculate_output(self, magnitudelist: List[float]):
        xmesh, ymesh = self.xmesh, self.ymesh
        for func, magnitude in zip(self.funclist, magnitudelist):
            xmesh, ymesh = func(xmesh, ymesh, magnitude)

        xmesh = xmesh.astype(int) % img.width
        ymesh = ymesh.astype(int) % img.height
        np_img = np.array(img)
        np_img = np_img[ymesh.flatten(), xmesh.flatten()].reshape(np_img.shape)
        return Image.fromarray(np_img)

    def _generate_mesh(self):
        self.xmesh, self.ymesh = np.meshgrid(
            np.arange(img.width), np.arange(img.height), sparse=False
        )
        self.reset_cache()


def transform(img, funclist, magnitudelist):
    xmesh, ymesh = np.meshgrid(
        np.arange(img.width), np.arange(img.height), sparse=False
    )
    for func, magnitude in zip(funclist, magnitudelist):
        xmesh, ymesh = func(xmesh=xmesh, ymesh=ymesh, magnitude=magnitude)

    xmesh = xmesh.astype(int) % img.width
    ymesh = ymesh.astype(int) % img.height
    np_img = np.array(img)
    np_img = np_img[ymesh.flatten(), xmesh.flatten()].reshape(np_img.shape)
    return Image.fromarray(np_img)


if __name__ == "__main__":
    img = Image.open("./test_images/img2.jpg")
    transformer = Motion_Transformer(img)
    result = transformer.calculate_output([0.5, 0.5, 0.5])
    result.show()
