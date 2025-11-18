from board_generation.board import Board
import numpy as np
from numpy.typing import NDArray


class OpenedBoard(Board):
    """
    An opened board is a board which has an already revealed start cell. This prevents the player from hitting a mine
    on their first click which is typically considered as undesirable game behavior.
    """

    def __init__(self, width: int, height: int, amount_mines: int, start_cell: tuple[int, int]):
        super().__init__(width=width, height=height, amount_mines=amount_mines)
        self.start_cell: tuple[int, int] = start_cell
        self.start_x, self.start_y = self.start_cell
        self.get_cell(self.start_x, self.start_y).revealed = True
        mine_indexes: list[tuple[int, int]] = self.__place_mines()
        self._adjust_numbers(mine_indexes=mine_indexes)

    def __place_mines(self) -> list[tuple[int, int]]:
        """
        Chooses mine positions of the required amount by sampling randomly from a uniform distribution and places the
        mines on the board at those positions while avoiding the open start cell.
        """
        low: int = self.start_x + self.start_y * self.width + 1
        high: int = low + self.amount_cells - 1
        sample: NDArray[np.int64] = self._rng.choice(a=range(low, high), size=self.amount_mines, replace=False)
        mine_indexes: list[tuple[int, int]] = []
        for num in sample:
            index: tuple[int, int] = (num % self.width).item(), ((num // self.width) % self.height).item()
            x, y = index
            self.get_cell(x, y).value = -1
            self.get_cell(x, y).is_mine = True
            mine_indexes.append(index)
        return mine_indexes

    def __repr__(self) -> str:
        return f"Board(width={self.width}, height={self.height}, amount_mines={self.amount_mines}, start_cell={self.start_cell})"

    def __str__(self) -> str:
        board_str: str = np.array2string(
            np.asarray([[self.get_cell(x, y).value for x in range(self.width)] for y in range(self.height)]))
        return f"Width = {self.width} | Height = {self.height} | Amount of mines = {self.amount_mines} | Start cell = {self.start_cell}\n{board_str}"
