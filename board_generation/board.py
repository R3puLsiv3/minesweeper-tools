import numpy as np
from numpy.random import Generator
from abc import ABC
from dataclasses import dataclass


class Board(ABC):
    """
    A class representing a generic Minesweeper board. A Board is a 2-dimensional grid of cells with a specified
    width and height. Every cell contains a value from -1 to 8, where -1 denotes a mine and 0 to 8 represents
    the amount of mines next to the cell. This class provides the adjust_numbers method which calculates the
    correct values on the board for any given mine indexes.
    """

    # The maximum width or height a board may have.
    __MAX_LENGTH: int = 100

    def __init__(self, width: int, height: int, amount_mines: int) -> None:
        self.width = min(width, self.__MAX_LENGTH)
        self.height = min(height, self.__MAX_LENGTH)
        self.amount_cells: int = self.width * self.height
        self.amount_mines: int = min(amount_mines, self.amount_cells - 1)
        self.board: list[list[Cell]] = [[Cell(x, y) for y in range(self.height)] for x in range(self.width)]
        self._rng: Generator = np.random.default_rng()

    def _adjust_numbers(self, mine_indexes: list[tuple[np.int64, np.int64]]) -> None:
        """
        Adjusts the values next to mines to the amount of mines they neighbor.
        """
        offsets: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for x, y in mine_indexes:
            for x_offset, y_offset in offsets:
                neighbor_x, neighbor_y = x + x_offset, y + y_offset
                if (0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height
                        and not self.board[neighbor_x][neighbor_y].is_mine):
                    self.board[neighbor_x][neighbor_y].value += 1


@dataclass
class Cell:
    x: int
    y: int
    value: int = 0
    is_mine: bool = False
    revealed: bool = False
    flagged: bool = False
