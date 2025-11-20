from typing import Final
from board_generation import generate_board, BoardTypes, ClosedBoard, OpenedBoard

# The maximum width or height a board may have.
MAX_LENGTH: Final[int] = 100

# To help access neighboring cells quickly.
OFFSETS: Final[list[tuple[int, int]]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

# An Expert closed board for testing.
EXPERT_BOARD_CLOSED: Final[ClosedBoard] = generate_board(width=30, height=16, amount_mines=99,
                                                         board_type=BoardTypes.CLOSED)
# An Expert opened board for testing.
EXPERT_BOARD_OPENED: Final[OpenedBoard] = generate_board(width=30, height=16, amount_mines=99,
                                                         board_type=BoardTypes.OPENED,
                                                         start_cell=(0, 0))
