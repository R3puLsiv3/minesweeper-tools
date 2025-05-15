import numpy as np
from numpy.random import Generator
from numpy.typing import NDArray
from abc import ABC, abstractmethod


class Board(ABC):
    """
    An abstract class representing a generic Minesweeper board. A Board is a 2-dimensional grid with a specified
    width and height. It contains a given number of mines with the rest of the cells being numbers from 0 to 8.
    Every number represents the amount of mines around the cell it occupies. This class provides the adjust_numbers
    method which calculates the correct numbers on the board for any given mine indexes.
    """

    # The maximum width or height a board may have.
    MAX_LENGTH: int = 100

    def __init__(self, size: tuple[int, int], amount_mines: int) -> None:
        desired_width, desired_height = size
        self.size: tuple[int, int] = (min(desired_width, self.MAX_LENGTH), min(desired_height, self.MAX_LENGTH))
        self.width, self.height = self.size
        self.amount_cells: int = self.width * self.height
        self.amount_mines: int = min(amount_mines, self.amount_cells - 1)
        self.board: NDArray[np.int8] = np.zeros(shape=(self.height, self.width), dtype=np.int8)
        self.rng: Generator = np.random.default_rng()

    @abstractmethod
    def generate_board(self) -> None:
        pass

    def adjust_numbers(self, mine_indexes: list[tuple[int, int]]) -> None:
        """
        Adjusts the numbers next to mines to the amount of mines they touch.
        """
        offsets: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for row, col in mine_indexes:
            for row_offset, col_offset in offsets:
                neighbor_row, neighbor_col = row + row_offset, col + col_offset
                if (0 <= neighbor_row < self.height and 0 <= neighbor_col < self.width
                        and self.board[neighbor_row, neighbor_col] != -1):
                    self.board[neighbor_row, neighbor_col] += 1
