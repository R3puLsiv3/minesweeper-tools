import numpy as np
from numpy.random import Generator
from dataclasses import dataclass
from config import MAX_LENGTH, OFFSETS
from typing import Iterator


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


class Board:
    """
    A class representing an empty Minesweeper board. A Board is a 2-dimensional grid of cells with a specified
    width and height. Since every board is entirely defined by the placement of its mines, this class provides the
    place_mine and remove_mine methods to edit the board while ensuring the correctness of the board.

    :param width: Amount of cells along the x-axis.
    :type width: int
    :param height: Amount of cells along the y-axis.
    :type height: int
    """

    def __init__(self, width: int, height: int, revealed: bool = False) -> None:
        self.width: int = max(1, min(width, MAX_LENGTH))
        self.height: int = max(1, min(height, MAX_LENGTH))
        self.amount_cells: int = self.width * self.height
        self.amount_mines: int = 0
        self.__cells: list[list[Cell]] = [[Cell(x, y, revealed=revealed) for x in range(self.width)] for y in
                                          range(self.height)]
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
        for neighbor_cell in self.get_neighbors(cell):
            if not neighbor_cell.is_mine:
                neighbor_cell.value += 1

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
        for neighbor_cell in self.get_neighbors(cell):
            if not neighbor_cell.is_mine:
                neighbor_cell.value -= 1
            else:
                cell.value += 1

    def get_neighbors(self, cell: Cell) -> Iterator[Cell]:
        """
        Generates the neighbors of a given cell.

        :param cell: Cell whose neighbors are requested.
        :type cell: Cell
        :return: Iterator over the neighbors of the cell.
        :rtype: Iterator[Cell]
        """
        for x_offset, y_offset in OFFSETS:
            neighbor_x, neighbor_y = cell.x + x_offset, cell.y + y_offset
            if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
                neighbor_cell: Cell = self.get_cell(neighbor_x, neighbor_y)
                yield neighbor_cell

    def __repr__(self) -> str:
        return f"Board(width={self.width}, height={self.height}, amount_mines={self.amount_mines})"

    def __str__(self) -> str:
        board_str: str = np.array2string(
            np.asarray([[self.get_cell(x, y).value for x in range(self.width)] for y in range(self.height)]))
        return f"Width = {self.width} | Height = {self.height} | Amount of mines = {self.amount_mines}\n{board_str}"
