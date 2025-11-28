from typing import Final

# The maximum width or height a board may have.
MAX_LENGTH: Final[int] = 100

# Default size of a cell in Minesweeper game.
CELL_LENGTH: Final[int] = 32

PADDING: Final[int] = 50

OPTIONS_PADDING: Final[int] = 10

OPTION_WIDTH: Final[int] = 50

OPTION_HEIGHT: Final[int] = 30

OPTIONS_WIDTH: Final[int] = 2 * OPTIONS_PADDING + OPTION_WIDTH

OPTIONS_HEIGHT: Final[int] = 4 * OPTIONS_PADDING + 3 * OPTION_HEIGHT

OPTIONS_X: Final[int] = PADDING

OPTIONS_Y: Final[int] = PADDING

BOARD_X = OPTIONS_WIDTH + 2 * PADDING

BOARD_Y = PADDING

TEXT_ENTRY_WIDTH_X = OPTIONS_X + OPTIONS_PADDING

TEXT_ENTRY_WIDTH_Y = OPTIONS_Y + OPTIONS_PADDING

TEXT_ENTRY_HEIGHT_X = OPTIONS_X + OPTIONS_PADDING

TEXT_ENTRY_HEIGHT_Y = TEXT_ENTRY_WIDTH_Y + OPTIONS_PADDING + OPTION_HEIGHT

BUTTON_CREATE_X = OPTIONS_X + OPTIONS_PADDING

BUTTON_CREATE_Y = TEXT_ENTRY_HEIGHT_Y + OPTIONS_PADDING + OPTION_HEIGHT

# To help access neighboring cells quickly.
OFFSETS: Final[list[tuple[int, int]]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
