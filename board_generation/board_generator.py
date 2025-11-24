from board_generation.board import Board
from board_generation.closed_board import ClosedBoard
from board_generation.opened_board import OpenedBoard
from board_generation.no_guess_board import NoGuessBoard
from enum import Enum


class BoardTypes(Enum):
    CLOSED = 1
    OPENED = 2
    NO_GUESS = 3
    EDITOR = 4


def generate_board(width: int, height: int, amount_mines: int = 0, board_type: BoardTypes = BoardTypes.EDITOR,
                   start_cell: tuple[int, int] = (0, 0)) -> Board | ClosedBoard | OpenedBoard | NoGuessBoard:
    """
    This is a board generator function that is intended as the user interface of the board generation package. Users
    can choose from four different Minesweeper boards:
        - An Editor Board which has no mines and where all the cells are revealed.
        - A Closed Board which has no specified start cell.
        - An Opened Board which has a specified start cell.
        - A No-Guess Board with a specified start cell from which the board can be solved without guessing.

    :param width: Amount of tiles along the x-axis.
    :type width: int
    :param height: Amount of tiles along the y-axis.
    :type height: int
    :param amount_mines: Amount of mines on the board.
    :type amount_mines: int
    :param board_type: Type of the board.
    :type board_type: BoardTypes
    :param start_cell: (x,y)-coordinate of the start cell on the board.
    :type start_cell: tuple[int, int]
    :return: Board which is specified by the given parameters.
    :rtype: Board | ClosedBoard | OpenedBoard | NoGuessBoard
    """
    match board_type:
        case BoardTypes.CLOSED:
            return ClosedBoard(width=width, height=height, amount_mines=amount_mines)
        case BoardTypes.OPENED:
            return OpenedBoard(width=width, height=height, amount_mines=amount_mines, start_cell=start_cell)
        case BoardTypes.NO_GUESS:
            return NoGuessBoard(width=width, height=height, amount_mines=amount_mines, start_cell=start_cell)
        case BoardTypes.EDITOR:
            return Board(width=width, height=height, revealed=True)
