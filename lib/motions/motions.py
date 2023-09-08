import math
from enum import Enum, auto
from typing import Callable, Iterable, Tuple

import numpy as np
from numpy.typing import NDArray
from PIL import Image


class PIXEL_INTERPOLATION_METHOD(Enum):
    """Automatically assign the integer value to the PIXEL_INTERPOLATION_METHOD."""

    INTEGER = auto()


class OFF_CANVAS_FILL(Enum):
    """Automatically assign the integer value to the OFF_CANVAS_FILL."""

    WRAP = auto()
    MIRROR = auto()
    EDGE = auto()


class Effect:
    """Effect class for all effects"""

    @staticmethod
    def explode(
        xmesh: NDArray, ymesh: NDArray, magnitude: float = 1
    ) -> Tuple[np.meshgrid, np.meshgrid]:
        """
        Explodes Image

        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for explode
        :return: xmesh, ymesh
        """
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
    def vertical_wave(
        xmesh: NDArray, ymesh: NDArray, wavenum: float = 1.5, magnitude: float = 1
    ) -> Tuple[np.meshgrid, np.meshgrid]:
        """
        Add vertical waves to Image

        :param wavenum: number of waves
        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for vertical waves
        :return: xmesh, ymesh
        """
        height, width = xmesh.shape
        offset = np.sin(xmesh / width * math.pi * 2 * wavenum) * magnitude * height / 4
        return xmesh, ymesh + offset

    @staticmethod
    def horizontal_wave(
        xmesh: NDArray, ymesh: NDArray, wavenum: float = 1.5, magnitude: float = 1
    ) -> Tuple[np.meshgrid, np.meshgrid]:
        """
        Add horizontal waves to Image

        :param wavenum: number of waves
        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for horizontal waves
        :return: xmesh, ymesh
        """
        height, width = xmesh.shape
        offset = np.sin(ymesh / height * math.pi * 2 * wavenum) * magnitude * width / 4
        return xmesh + offset, ymesh

    @staticmethod
    def vertical_spike(
        xmesh: NDArray, ymesh: NDArray, spikenum: float = 5, magnitude: float = 1
    ) -> Tuple[np.meshgrid, np.meshgrid]:
        """
        Add vertical spikes to Image

        :param spikenum: number of spikes
        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for vertical spikes
        :return: xmesh, ymesh
        """
        _, width = xmesh.shape
        spike_distance = width // spikenum
        offset = np.abs(xmesh % spike_distance - spike_distance // 2) * magnitude * 2
        return xmesh, ymesh + offset

    @staticmethod
    def horizontal_spike(
        xmesh: NDArray, ymesh: NDArray, spikenum: float = 5, magnitude: float = 1
    ) -> Tuple[np.meshgrid, np.meshgrid]:
        """
        Add horizontal spikes to Image

        :param spikenum: number of spikes
        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for horizontal spikes
        :return: xmesh, ymesh
        """
        height, _ = xmesh.shape
        spike_distance = height // spikenum
        offset = np.abs(ymesh % spike_distance - spike_distance // 2) * magnitude * 2
        return xmesh + offset, ymesh


class Motion_Transformer:
    """A class for motion transformation"""

    def __init__(
        self,
        img: Image.Image,
        interpolation: PIXEL_INTERPOLATION_METHOD = PIXEL_INTERPOLATION_METHOD.INTEGER,
        fill_method: OFF_CANVAS_FILL = OFF_CANVAS_FILL.MIRROR,
        funclist: Iterable[Callable] = (
            Effect.horizontal_wave,
            Effect.horizontal_spike,
            Effect.vertical_wave,
        ),
    ) -> None:
        self.img = img
        self.interpolation = interpolation
        self.fill_method = fill_method
        self.funclist = funclist
        self._generate_mesh()
        self.xmesh: NDArray
        self.ymesh: NDArray

    def reset_cache(self) -> None:
        """
        Reset the cache

        :return:
        """
        self.cache: dict = {}

    def update_image(self, img: Image) -> None:
        """
        Update the image

        :param img: the image
        :return:
        """
        if img.shape != self.img.shape:
            self._generate_mesh()
        self.img = img

    def calculate_output(self, magnitudelist: Iterable[float]) -> Image.Image:
        """
        Calculate the output

        :param magnitudelist: the list of magnitudes
        :return:
        """
        xmesh, ymesh = self.xmesh, self.ymesh
        for func, magnitude in zip(self.funclist, magnitudelist):
            xmesh, ymesh = func(xmesh, ymesh, magnitude)
        xmesh = xmesh.astype(int) % img.width
        ymesh = ymesh.astype(int) % img.height
        np_img = np.array(img)
        np_img = np_img[ymesh.flatten(), xmesh.flatten()].reshape(np_img.shape)
        return Image.fromarray(np_img)

    def _generate_mesh(self) -> None:
        """
        Generate the mesh

        :return:
        """
        self.xmesh, self.ymesh = np.meshgrid(
            np.arange(img.width), np.arange(img.height), sparse=False
        )
        self.reset_cache()


def transform(
    img: Image.Image, funclist: Iterable[Callable], magnitudelist: Iterable[float]
) -> Image.Image:
    """
    Transform the image

    :param img: the image
    :param funclist: the list of functions
    :param magnitudelist: the list of magnitudes
    :return:
    """
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
    img = Image.open("dahlias.jpg")
    transformer = Motion_Transformer(img)
    result = transformer.calculate_output([0.5, 0.5, 0.5])
    result.show()
