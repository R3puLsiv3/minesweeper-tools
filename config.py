from typing import Final

# The maximum width or height a board may have.
MAX_LENGTH: Final[int] = 100

# Default size of a cell in Minesweeper game.
CELL_LENGTH: Final[int] = 32

# To help access neighboring cells quickly.
OFFSETS: Final[list[tuple[int, int]]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
