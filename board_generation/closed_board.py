from board_generation.board import Board
import numpy as np
from numpy.typing import NDArray


class ClosedBoard(Board):
    """
    A closed board is a board which has no revealed cells. The player may hit a mine on their first click which is
    usually not considered to be enjoyable from a gameplay perspective.

    :param width: Amount of tiles along the x-axis.
    :type width: int
    :param height: Amount of tiles along the y-axis.
    :type height: int
    :param amount_mines: Amount of mines on the board.
    :type amount_cells: int
    """

    def __init__(self, width: int, height: int, amount_mines: int):
        super().__init__(width=width, height=height)
        amount_mines = max(0, min(amount_mines, self.amount_cells))
        self.__place_mines(amount_mines)

    def __place_mines(self, amount_mines: int) -> None:
        """
        Chooses mine positions of the required amount by sampling randomly from a uniform distribution and places the
        mines on the board at those positions.
        """
        sample: NDArray[np.int64] = self._rng.choice(a=range(0, self.amount_cells), size=amount_mines,
                                                     replace=False)
        mine_indexes = [((num % self.width).item(), (num // self.width).item()) for num in sample]
        for x, y in mine_indexes:
            self.place_mine(x, y)

    def __repr__(self) -> str:
        return f"Board(width={self.width}, height={self.height}, amount_mines={self.amount_mines})"

    def __str__(self) -> str:
        board_str: str = np.array2string(
            np.asarray([[self.get_cell(x, y).value for x in range(self.width)] for y in range(self.height)]))
        return f"Width = {self.width} | Height = {self.height} | Amount of mines = {self.amount_mines}\n{board_str}"
