from pathlib import Path
from typing import Dict, List, Tuple, cast

from PyQt6.QtCore import Qt

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
            return Path(image_dir_path, "clockwork.jpg")
        if self.level_number == 3:
            return Path(image_dir_path, "number_hidden_image.png")
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
            return "secret2"
        if self.level_number == 3:
            return "Very secret"
        if self.level_number == 4:
            return "200012"
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
                                ("A", (0, 100), Qt.Orientation.Horizontal),
                                ("B", (0, 100), Qt.Orientation.Horizontal),
                            ],
                            "dropdowns": [],
                            "description": "This is a description"
                        }
                    ),
                    {
                        "second_image": None,
                        "secret_code": "42",
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
                                )
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
                        }
                    ),
                    {
                        "second_image": Path(image_dir_path, "doggo.jpg"),
                        "secret_code": "secret",
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
                                [
                                    "Rust",
                                    "Chocolate",
                                    "Flamenco",
                                    "Casablanca",
                                    "Buff"
                                ]
                            ],
                            "buttons": [
                                1  # TODO MAKE THIS HAVE INFO
                            ],
                            "description": "This is a description"
                        }
                    ),
                    {}
                )
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
