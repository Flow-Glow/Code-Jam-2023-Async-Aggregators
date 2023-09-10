from pathlib import Path
from typing import Dict, List, Tuple, cast

from PIL import Image
from PyQt6.QtCore import Qt

from lib.motions.motions import MotionTransformer
from src.control_panel import ControlPanel

FilterItem = Tuple[Path, ControlPanel, Dict[str, Path | str | None | int]]
FilterList = List[FilterItem]


class Level:
    """Class to represent a level in the game."""

    def __init__(self, level_number: int):
        self.level_number = level_number
        self.secret_answer = self.get_secret_answer()
        self.img_source = self.get_image_source()
        self.filters = self.get_filters()

    def get_image_source(self) -> Path:
        """
        Get the image source for the level

        :return: Path of the image file
        """
        # This can be extended to retrieve images dynamically based on the level
        image_dir_path = Path(Path(__file__).parent, "images")
        if self.level_number == 1:
            return Path(image_dir_path, "reverse_ishihara.png")
        if self.level_number == 2:
            return Path(image_dir_path, "snake.png")
        if self.level_number == 3:
            return Path(image_dir_path, "number_hidden_image.png")
        if self.level_number == 4:
            return Path(image_dir_path, "desert.jpg")
        if self.level_number == 5:
            return Path(image_dir_path, "img2.jpg")
        return Path(image_dir_path, "default.png")

    def get_secret_answer(self) -> str:
        """
        Get the secret answer for the level

        :return: secret string
        """
        # This can be extended to provide answers dynamically based on the level
        if self.level_number == 1:
            return "42"
        if self.level_number == 2:
            return "snake_case"
        if self.level_number == 3:
            return "200012"
        if self.level_number == 4:
            return "obfuscation"
        if self.level_number == 5:
            return "secret"
        return "pythoncodejam2023"

    def get_filters(self) -> FilterList:
        """
        Get the filters for the level

        :return: list of filters
        """
        # This can be extended to provide filters dynamically based on the level

        icons_dir_path = Path(Path(__file__).parent, "icons")
        image_dir_path = Path(Path(__file__).parent, "images")
        filters = [
            [
                (
                    Path(icons_dir_path, "rishihara.png"),
                    ControlPanel(
                        "Ishihara",
                        {
                            "sliders": [
                                ("A", (0, 100), Qt.Orientation.Horizontal, True),
                                ("B", (0, 100), Qt.Orientation.Horizontal, True),
                            ],
                            "dropdowns": [],
                            "description": "Within the confines of a digital realm, "
                                           "a cryptic puzzle materializes on the screen. "
                                           "It appears as a static image, unassuming at first glance. "
                                           "Yet, in this virtual world, the challenge is no less mysterious."
                                           "A seemingly ordinary image, pixel by pixel, conceals a hidden code. "
                                           "To unlock its secrets, you must change the image itself. "
                                           "With each  alteration, the pixels shift, "
                                           "rearranging themselves into a new configuration. "
                                           "The code, ever elusive, lurks just beneath the surface, "
                                           "waiting to be discovered."
                        },
                    ),
                    {
                        "second_image": None,
                        "secret_code": "42",
                        "MotionTransformer": None,
                    },
                ),
            ],
            [
                (
                    Path(icons_dir_path, "button_sample2.png"),
                    ControlPanel(
                        "Double Exposure",
                        {
                            "sliders": [
                                (
                                    "Exposure",
                                    ("Image 1", "Image 2"),
                                    Qt.Orientation.Horizontal,
                                    False,
                                )
                            ],
                            "dropdowns": [],
                            "description": "Within the shadowy depths of the digital realm, a mysterious symbol "
                                           "weaves a cryptic tale. As you tread cautiously through this enigmatic "
                                           "landscape, look beyond the obvious, for the answer lies in the "
                                           "unspoken_connector that guides the way. What compound_word emerges from "
                                           "the darkness, uniting the virtual and the tangible with its "
                                           "discreet_presence?"
                        },
                    ),
                    {
                        "second_image": Path(image_dir_path, "cases.jpeg"),
                        "secret_code": "snake_case",
                        "MotionTransformer": None,
                    },
                ),
            ],
            [
                (
                    Path(icons_dir_path, "button_sample4.png"),
                    ControlPanel(
                        "Color Swap",
                        {
                            "sliders": [],
                            "dropdowns": [
                                ["Rust", "Chocolate", "Flamenco", "Casablanca", "Buff"]
                            ],
                            "description": "The code is a lifeline, a thread of order within the digital chaos, "
                                           "a signal in the noise. "
                                           "As you decrypt its meaning, "
                                           "you can't help but wonder what secrets it holds, "
                                           "what mysteries it guards. "
                                           "The digital world stretches out before you, "
                                           "a labyrinth of information and intrigue, "
                                           "daring you to continue your quest, "
                                           "to unravel the enigma hidden within the noisy image.",
                            "combo_box_buttons": ["swap"],
                        },

                    ),
                    {},
                )
            ],
            [
                (
                    Path(icons_dir_path, "magnifying_glass.png"),
                    ControlPanel(
                        "Hidden in ASCII",
                        {
                            "sliders": [],
                            "dropdowns": [],
                            "description": "In the enigmatic world of 'Digital Shadows,' you're not just a player; "
                                           "you're an intrepid explorer of the digital frontier. As you venture "
                                           "through hidden corners of the web, you'll encounter mysterious images "
                                           "that seem to whisper hidden truths. In this realm, secrets are veiled "
                                           "within intricate patterns, waiting for the discerning eye to unravel "
                                           "their significance. But remember, to truly understand, you must 'look "
                                           "under a different eye,' unveiling the cryptic messages concealed in these "
                                           "enigmatic visuals. Only then can you gain passage to the deeper layers of "
                                           "underground hacker dens, forgotten warehouses, and secure safe houses. "
                                           "Decoding these clandestine messages is your ticket to unlocking the next "
                                           "level of intrigue. Are you ready to uncover the secrets lurking in the "
                                           "Digital Shadows?",
                            "buttons": ["Unlock Digital Glyphs"]
                        }
                    ),
                    {},
                )
            ],
            [
                (
                    Path(icons_dir_path, "motion_icon.png"),
                    ControlPanel(
                        "Motion",
                        {
                            "sliders": [
                                (
                                    "horizontal wave",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False,
                                ),
                                (
                                    "vertical wave",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False,
                                ),
                                (
                                    "vertical spike",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False,
                                ),
                                (
                                    "horizontal spike",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False,
                                ),
                                ("explode", (0, 100), Qt.Orientation.Horizontal, False),
                            ],
                            "dropdowns": [],
                            "description": "We were unable to finish this level, "
                                           "but we really liked this image editing functionality."
                                           "Thanks for playing!"
                        },
                    ),
                    {
                        "second_image": None,
                        "secret_code": "Picasso",
                        "MotionTransformer": MotionTransformer(
                            Image.open(image_dir_path / "img2.jpg")
                        ),
                    },
                ),
            ]
        ]

        if 0 <= self.level_number - 1 < len(filters):
            return cast(FilterList, filters[self.level_number - 1])
        else:
            # Return an empty FilterList if out-of-bounds
            return []

    def level_up(self) -> 'Level':
        """
        Level up the game

        :return: None
        """
        return Level(self.level_number + 1)
