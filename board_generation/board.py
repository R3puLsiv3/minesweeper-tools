import numpy as np
from numpy.random import Generator
from abc import ABC
from dataclasses import dataclass
from typing import Final

# The maximum width or height a board may have.
MAX_LENGTH: Final[int] = 100

# To access neighboring cells quickly when adding or removing a mine.
OFFSETS: Final[list[tuple[int, int]]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


@dataclass
class Cell:
    """
    A class representing a single cell of a Minesweeper board. Every cell contains a value from -1 to 8, where -1
    denotes a mine and 0 to 8 represents the amount of mines neighboring the cell. The x-value grows to the right
    and the y-value towards the bottom of the board. Meaning, that the top-left corner has the index (0, 0) and the
    bottom-right corner has the index (board.width - 1, board.height - 1).

    :param x: Position on the x-axis.
    :type x: int
    :param y: Position on the y-axis.
    :type y: int
    :param value: Value of the cell.
    :type value: int
    :param is_mine: Whether the cell is a mine or not.
    :type is_mine: bool
    :param revealed: Whether the cell is opened or not.
    :type revealed: bool
    :param flagged: Whether the cell is flagged or not.
    :type flagged: bool
    """
    x: int
    y: int
    value: int = 0
    is_mine: bool = False
    revealed: bool = False
    flagged: bool = False

    def set_mine(self) -> None:
        self.value = -1
        self.is_mine = True

    def set_empty(self) -> None:
        self.value = 0
        self.is_mine = False


class Board(ABC):
    """
    A class representing a generic Minesweeper board. A Board is a 2-dimensional grid of cells with a specified
    width and height. Since every board is entirely defined by the placement of its mines, this class provides the
    place_mine and remove_mine methods to edit the board while ensuring the correctness of the board.

    :param width: Amount of tiles along the x-axis.
    :type width: int
    :param height: Amount of tiles along the y-axis.
    :type height: int
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = max(1, min(width, MAX_LENGTH))
        self.height = max(1, min(height, MAX_LENGTH))
        self.amount_cells: int = self.width * self.height
        self.amount_mines: int = 0
        self.__cells: list[list[Cell]] = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        self._rng: Generator = np.random.default_rng()

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Provides access to the cell on the board at the given (x,y)-coordinate.

        :param x: Position on the x-axis.
        :type x: int
        :param y: Position on the y-axis.
        :type y: int
        :return: Cell on the board at the (x,y)-coordinate.
        :rtype: Cell
        """
        return self.__cells[y][x]

    def place_mine(self, x: int, y: int) -> None:
        """
        Places a mine on the board at the cell which corresponds to the given (x,y)-coordinate while ensuring the
        correctness of the board.

        :param x: Position on the x-axis.
        :type x: int
        :param y: Position on the y-axis.
        :type y: int
        """
        cell = self.get_cell(x, y)
        if cell.is_mine:
            return
        cell.set_mine()
        self.amount_mines += 1
        for x_offset, y_offset in OFFSETS:
            neighbor_x, neighbor_y = x + x_offset, y + y_offset
            if (0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height
                    and not self.get_cell(neighbor_x, neighbor_y).is_mine):
                self.get_cell(neighbor_x, neighbor_y).value += 1

    def remove_mine(self, x: int, y: int) -> None:
        """
        Removes a mine on the board at the cell which corresponds to the given (x,y)-coordinate while ensuring the
        correctness of the board.

        :param x: Position on the x-axis.
        :type x: int
        :param y: Position on the y-axis.
        :type y: int
        """
        cell = self.get_cell(x, y)
        if not cell.is_mine:
            return
        cell.set_empty()
        self.amount_mines -= 1
        for x_offset, y_offset in OFFSETS:
            neighbor_x, neighbor_y = x + x_offset, y + y_offset
            if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
                if not self.get_cell(neighbor_x, neighbor_y).is_mine:
                    self.get_cell(neighbor_x, neighbor_y).value -= 1
                else:
                    cell.value += 1
