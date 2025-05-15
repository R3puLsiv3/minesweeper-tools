from closed_board import ClosedBoard
from opened_board import OpenedBoard
from no_guess_board import NoGuessBoard
from enum import Enum


class BoardTypes(Enum):
    CLOSED = 1
    OPENED = 2
    NO_GUESS = 3


def generate_board(size: tuple[int, int], amount_mines: int, board_type: BoardTypes = BoardTypes.CLOSED,
                   start_cell: tuple[int, int] = (0, 0)) -> Board:
    match board_type:
        case BoardTypes.CLOSED:
            return ClosedBoard(size=size, amount_mines=amount_mines)
        case BoardTypes.OPENED:
            return OpenedBoard(size=size, amount_mines=amount_mines, start_cell=start_cell)
        case BoardTypes.NO_GUESS:
            return NoGuessBoard(size=size, amount_mines=amount_mines, start_cell=start_cell)
