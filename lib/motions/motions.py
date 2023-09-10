import math
from collections import OrderedDict
from enum import Enum, auto
from typing import Callable, Iterable

import numpy as np
from numpy.typing import NDArray
from PIL import Image

np.seterr(divide="ignore", invalid="ignore")


class PIXEL_INTERPOLATION_METHOD(Enum):
    """
    Interperlation methods for targets between pixels

    Allows you to select a method used to resolve a non-integer pixel value
    after all motions are complete.  Potentially doing a mix of surrounding
    pixels.
    """

    INTEGER = auto()


class OFF_CANVAS_FILL(Enum):
    """Methods used to fill pixels from outside the image canvas"""

    WRAP = auto()
    MIRROR = auto()
    EDGE = auto()


class Effect:
    """List of effects that all take xmesh, ymesh, and magnitude of the effect"""

    @staticmethod
    def vertical_wave(
        xmesh: NDArray, ymesh: NDArray, magnitude: float = 1, wavenum: float = 1.5
    ) -> tuple[NDArray, NDArray]:
        """
        Add vertical waves to Image

        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for vertical waves
        :param wavenum: number of waves
        :return: xmesh, ymesh
        """
        height, width = xmesh.shape
        offset = np.sin(xmesh / width * math.pi * 2 * wavenum) * magnitude * height / 4
        return xmesh, ymesh + offset

    @staticmethod
    def horizontal_wave(
        xmesh: NDArray, ymesh: NDArray, magnitude: float = 1, wavenum: float = 1.5
    ) -> tuple[NDArray, NDArray]:
        """
        Add horizontal waves to Image

        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for horizontal waves
        :param wavenum: number of waves
        :return: xmesh, ymesh
        """
        height, width = xmesh.shape
        offset = np.sin(ymesh / height * math.pi * 2 * wavenum) * magnitude * width / 4
        return xmesh + offset, ymesh

    @staticmethod
    def vertical_spike(
        xmesh: NDArray, ymesh: NDArray, magnitude: float = 1, spikenum: float = 5
    ) -> tuple[NDArray, NDArray]:
        """
        Add vertical spikes to Image

        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for vertical spikes
        :param spikenum: number of spikes
        :return: xmesh, ymesh
        """
        _, width = xmesh.shape
        spike_distance = width // spikenum
        offset = np.abs(xmesh % spike_distance - spike_distance // 2) * magnitude * 2
        return xmesh, ymesh + offset

    @staticmethod
    def horizontal_spike(
        xmesh: NDArray, ymesh: NDArray, magnitude: float = 1, spikenum: float = 5
    ) -> tuple[NDArray, NDArray]:
        """
        Add horizontal spikes to Image

        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude for horizontal spikes
        :param spikenum: number of spikes
        :return: xmesh, ymesh
        """
        height, _ = xmesh.shape
        spike_distance = height // spikenum
        offset = np.abs(ymesh % spike_distance - spike_distance // 2) * magnitude * 2
        return xmesh + offset, ymesh

    @staticmethod
    def explode(
        xmesh: NDArray, ymesh: NDArray, magnitude: float = 1
    ) -> tuple[NDArray, NDArray]:
        """
        Creates a motion outward from the center

        :param xmesh: a mesh grid for x-axis
        :param ymesh: a mesh grid for y-axis
        :param magnitude: the magnitude of the effect
        :return: xmesh, ymesh
        """
        height, width = xmesh.shape
        normalized_distance = (
            (2 * xmesh / width - 1) ** 2 + (2 * ymesh / height - 1) ** 2
        ) ** 0.5
        new_distance = normalized_distance / (
            np.maximum(
                (1.5 - normalized_distance) * 3 * (abs(magnitude) + 0.000001) ** 0.8
                + 0.2,
                1,
            )
            + 0.0000001
        )
        xmesh = (xmesh - width / 2) * new_distance / normalized_distance + width / 2
        ymesh = (ymesh - height / 2) * new_distance / normalized_distance + height / 2
        return xmesh, ymesh


def explode(
    xmesh: NDArray, ymesh: NDArray, magnitude: float = 1
) -> tuple[NDArray, NDArray]:
    """
    Creates a motion outward from the center - work in progress

    :param xmesh: a mesh grid for x-axis
    :param ymesh: a mesh grid for y-axis
    :param magnitude: the magnitude of the effect
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


class MotionTransformer:
    """Processes all motion effects together to save on pre-processing and post-processing required for each"""

    def __init__(
        self,
        img: Image.Image,
        answer: str,
        interpolation: PIXEL_INTERPOLATION_METHOD = PIXEL_INTERPOLATION_METHOD.INTEGER,
        fill_method: OFF_CANVAS_FILL = OFF_CANVAS_FILL.MIRROR,
        funclist: Iterable[Callable] = (
            Effect.horizontal_wave,
            Effect.vertical_wave,
            Effect.vertical_spike,
            Effect.horizontal_spike,
            Effect.explode,
        ),
    ) -> None:
        self.img = img
        self.answer = answer
        self.interpolation = interpolation
        self.fill_method = fill_method
        self.funclist = tuple(funclist)
        self._generate_mesh()
        self.xmesh: NDArray
        self.ymesh: NDArray
        self.cache: OrderedDict[
            tuple[str, float], tuple[NDArray, NDArray]
        ] = OrderedDict()
        self.cache_capacity: int = 10

        self.offsets = []
        for letter in self.answer.upper():
            self.offsets.append(ord(letter)-65)

    def reset_cache(self) -> None:
        """
        Reset the cache of intermediate steps between effects

        :return:
        """
        self.cache = OrderedDict()

    def update_image(self, img: Image.Image) -> None:
        """
        Change the image to an alternative in case previous effects were updated

        :param img: the image
        :return:
        """
        if img.size != self.img.size:
            self._generate_mesh()
        self.img = img

    def calculate_output(self, magnitudelist: Iterable[float]) -> Image.Image:
        """
        Outputs the distorted image with all filters applied

        :param magnitudelist: the list of magnitudes
        :return:
        """
        xmesh, ymesh = self.xmesh, self.ymesh
        for func, magnitude, offset in zip(self.funclist, magnitudelist, self.offsets):
            xmesh, ymesh = func(xmesh, ymesh, (magnitude - offset) / 20)
        xmesh = xmesh.astype(int) % self.img.width
        ymesh = ymesh.astype(int) % self.img.height
        np_img = np.array(self.img)
        np_img = np_img[ymesh.flatten(), xmesh.flatten()].reshape(np_img.shape)
        return Image.fromarray(np_img)

    def _generate_mesh(self) -> None:
        """
        Generate the mesh grid all distortions will be applied to

        :return:
        """
        self.xmesh, self.ymesh = np.meshgrid(
            np.arange(self.img.width), np.arange(self.img.height), sparse=False
        )
        self.reset_cache()
