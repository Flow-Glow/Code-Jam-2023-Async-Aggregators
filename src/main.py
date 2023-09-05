import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

import level
import window

def main() -> None:
    """Main function"""
    app = QApplication(sys.argv)
    # Assuming the player is at level 1
    current_level = level.Level(1)
    game_window = window.Window(current_level)

    game_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
