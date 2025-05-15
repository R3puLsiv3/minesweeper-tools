from board import Board
import numpy as np
from numpy.typing import NDArray


class OpenedBoard(Board):

    def __init__(self, size: tuple[int, int], amount_mines: int, start_cell: tuple[int, int]):
        super().__init__(size=size, amount_mines=amount_mines)
        self.start_cell: tuple[int, int] = start_cell
        self.start_row, self.start_col = self.start_cell
        mine_indexes: list[tuple[np.int64, np.int64]] = self.__place_mines()
        self._adjust_numbers(mine_indexes=mine_indexes)

    def __place_mines(self) -> list[tuple[np.int64, np.int64]]:
        """
        Chooses mine positions of the required amount by sampling randomly from a uniform distribution and places the
        mines on the board at those positions while avoiding the open start cell.
        """
        low: int = self.start_row * self.height + self.start_col % self.width + 1
        high: int = low + self.amount_cells - 1
        sample: NDArray[np.int64] = self._rng.choice(a=range(low, high), size=self.amount_mines, replace=False)
        mine_indexes: list[tuple[np.int64, np.int64]] = []
        for num in sample:
            index: tuple[np.int64, np.int64] = (num // self.height) % self.height, num % self.width
            self.board[index] = -1
            mine_indexes.append(index)
        return mine_indexes
