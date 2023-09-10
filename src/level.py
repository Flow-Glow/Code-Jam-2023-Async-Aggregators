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
                                ("A", (0, 100), Qt.Orientation.Horizontal, True, 4),
                                ("B", (0, 100), Qt.Orientation.Horizontal, True, 8),
                            ],
                            "dropdowns": [],
                            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                                           "tempor incididunt ut labore et dolore magna aliqua. Nullam ac tortor "
                                           "vitae purus faucibus. Velit euismod in pellentesque massa placerat duis "
                                           "ultricies lacus sed. Et sollicitudin ac orci phasellus egestas tellus. "
                                           "Non blandit massa enim nec dui nunc mattis enim. Eu non diam phasellus "
                                           "vestibulum lorem sed risus ultricies. Nisl tincidunt eget nullam non nisi "
                                           "est sit amet facilisis. Nulla aliquet enim tortor at auctor urna nunc id. "
                                           "Facilisis magna etiam tempor orci eu lobortis. Purus gravida quis blandit "
                                           "turpis cursus. Feugiat pretium nibh ipsum consequat nisl vel pretium. "
                                           "Donec massa sapien faucibus et molestie. Pellentesque habitant morbi "
                                           "tristique senectus et netus et. Neque volutpat ac tincidunt vitae semper. "
                                           "Faucibus vitae aliquet nec ullamcorper sit amet risus nullam."
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
                                    0
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
                            "dropdowns": [
                                ["Rust", "Chocolate", "Flamenco", "Casablanca", "Buff"]
                            ],
                            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                                           "tempor incididunt ut labore et dolore magna aliqua. Nullam ac tortor "
                                           "vitae purus faucibus. Velit euismod in pellentesque massa placerat duis "
                                           "ultricies lacus sed. Et sollicitudin ac orci phasellus egestas tellus. "
                                           "Non blandit massa enim nec dui nunc mattis enim. Eu non diam phasellus "
                                           "vestibulum lorem sed risus ultricies. Nisl tincidunt eget nullam non nisi "
                                           "est sit amet facilisis. Nulla aliquet enim tortor at auctor urna nunc id. "
                                           "Facilisis magna etiam tempor orci eu lobortis. Purus gravida quis blandit "
                                           "turpis cursus. Feugiat pretium nibh ipsum consequat nisl vel pretium. "
                                           "Donec massa sapien faucibus et molestie. Pellentesque habitant morbi "
                                           "tristique senectus et netus et. Neque volutpat ac tincidunt vitae semper. "
                                           "Faucibus vitae aliquet nec ullamcorper sit amet risus nullam.",
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
                                    6
                                ),
                                (
                                    "vertical wave",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False,
                                    12
                                ),
                                (
                                    "vertical spike",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False,
                                    18
                                ),
                                (
                                    "horizontal spike",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False,
                                    10
                                ),
                                ("explode", (0, 100), Qt.Orientation.Horizontal, False, 12),
                            ],
                            "dropdowns": [],
                            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                                           "tempor incididunt ut labore et dolore magna aliqua. Nullam ac tortor "
                                           "vitae purus faucibus. Velit euismod in pellentesque massa placerat duis "
                                           "ultricies lacus sed. Et sollicitudin ac orci phasellus egestas tellus. "
                                           "Non blandit massa enim nec dui nunc mattis enim. Eu non diam phasellus "
                                           "vestibulum lorem sed risus ultricies. Nisl tincidunt eget nullam non nisi "
                                           "est sit amet facilisis. Nulla aliquet enim tortor at auctor urna nunc id. "
                                           "Facilisis magna etiam tempor orci eu lobortis. Purus gravida quis blandit "
                                           "turpis cursus. Feugiat pretium nibh ipsum consequat nisl vel pretium. "
                                           "Donec massa sapien faucibus et molestie. Pellentesque habitant morbi "
                                           "tristique senectus et netus et. Neque volutpat ac tincidunt vitae semper. "
                                           "Faucibus vitae aliquet nec ullamcorper sit amet risus nullam."
                        },
                    ),
                    {
                        "second_image": None,
                        "secret_code": "Turbo secret",
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

    def level_up(self) -> None:
        """
        Level up the game

        :return: None
        """
        self.level_number += 1
        self.secret_answer = self.get_secret_answer()
        self.img_source = self.get_image_source()
        self.filters = self.get_filters()
