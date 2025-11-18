from board_generation.board import Board
import numpy as np
from numpy.typing import NDArray


class ClosedBoard(Board):
    """
    A closed board is a board which has no revealed cells. The player may hit a mine on their first click which is
    usually not considered to be enjoyable from a gameplay perspective.
    """

    def __init__(self, width: int, height: int, amount_mines: int):
        super().__init__(width=width, height=height, amount_mines=amount_mines)
        mine_indexes: list[tuple[int, int]] = self.__place_mines()
        self._adjust_numbers(mine_indexes=mine_indexes)

    def __place_mines(self) -> list[tuple[int, int]]:
        """
        Chooses mine positions of the required amount by sampling randomly from a uniform distribution and places the
        mines on the board at those positions.
        """
        sample: NDArray[np.int64] = self._rng.choice(a=range(0, self.amount_cells), size=self.amount_mines,
                                                     replace=False)
        mine_indexes: list[tuple[int, int]] = []
        for num in sample:
            index: tuple[int, int] = (num % self.width).item(), (num // self.width).item()
            x, y = index
            self.get_cell(x, y).value = -1
            self.get_cell(x, y).is_mine = True
            mine_indexes.append(index)
        return mine_indexes

    def __repr__(self) -> str:
        return f"Board(width={self.width}, height={self.height}, amount_mines={self.amount_mines})"

    def __str__(self) -> str:
        board_str: str = np.array2string(
            np.asarray([[self.get_cell(x, y).value for x in range(self.width)] for y in range(self.height)]))
        return f"Width = {self.width} | Height = {self.height} | Amount of mines = {self.amount_mines}\n{board_str}"
