from board_generation.board import Board
from board_generation.closed_board import ClosedBoard
from board_generation.opened_board import OpenedBoard
from board_generation.no_guess_board import NoGuessBoard
from enum import Enum


class BoardTypes(Enum):
    CLOSED = 1
    OPENED = 2
    NO_GUESS = 3


def generate_board(width: int, height: int, amount_mines: int, board_type: BoardTypes = BoardTypes.CLOSED,
                   start_cell: tuple[int, int] = (0, 0)) -> ClosedBoard | OpenedBoard | NoGuessBoard:
    match board_type:
        case BoardTypes.CLOSED:
            return ClosedBoard(width=width, height=height, amount_mines=amount_mines)
        case BoardTypes.OPENED:
            return OpenedBoard(width=width, height=height, amount_mines=amount_mines, start_cell=start_cell)
        case BoardTypes.NO_GUESS:
            return NoGuessBoard(width=width, height=height, amount_mines=amount_mines, start_cell=start_cell)
