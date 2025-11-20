from board_generation.board import Board
import numpy as np
from numpy.typing import NDArray


class OpenedBoard(Board):
    """
    An opened board is a board which has an already revealed start cell. This prevents the player from hitting a mine
    on their first click which is typically considered as undesirable game behavior.

    :param width: Amount of tiles along the x-axis.
    :type width: int
    :param height: Amount of tiles along the y-axis.
    :type height: int
    :param amount_mines: Amount of mines on the board.
    :type amount_cells: int
    :param start_cell: (x,y)-coordinate of the start cell on the board.
    :type start_cell: tuple[int, int]
    """

    def __init__(self, width: int, height: int, amount_mines: int, start_cell: tuple[int, int]):
        super().__init__(width=width, height=height)
        self.start_cell: tuple[int, int] = start_cell
        self.start_x, self.start_y = self.start_cell
        self.get_cell(self.start_x, self.start_y).revealed = True
        amount_mines = max(0, min(amount_mines, self.amount_cells - 1))
        self.__place_mines(amount_mines)

    def __place_mines(self, amount_mines: int) -> None:
        """
        Chooses mine positions of the required amount by sampling randomly from a uniform distribution and places the
        mines on the board at those positions while avoiding the open start cell.
        """
        low: int = self.start_x + self.start_y * self.width + 1
        high: int = low + self.amount_cells - 1
        sample: NDArray[np.int64] = self._rng.choice(a=range(low, high), size=amount_mines, replace=False)
        mine_indexes = [((num % self.width).item(), ((num // self.width) % self.height).item()) for num in sample]
        for x, y in mine_indexes:
            self.place_mine(x, y)

    def __repr__(self) -> str:
        return f"Board(width={self.width}, height={self.height}, amount_mines={self.amount_mines}, start_cell={self.start_cell})"

    def __str__(self) -> str:
        board_str: str = np.array2string(
            np.asarray([[self.get_cell(x, y).value for x in range(self.width)] for y in range(self.height)]))
        return f"Width = {self.width} | Height = {self.height} | Amount of mines = {self.amount_mines} | Start cell = {self.start_cell}\n{board_str}"
