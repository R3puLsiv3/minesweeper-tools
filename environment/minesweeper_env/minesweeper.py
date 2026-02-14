import numpy as np
from numpy.random import Generator
from numpy.typing import NDArray
from tabulate import tabulate


class Minesweeper:

    def __init__(self, rows: int, cols: int, amount_mines: int, start_row=0, start_col=0,
                 seed: int | None = None):
        self.rows = rows
        self.cols = cols
        self.amount_mines = amount_mines
        self.start_row, self.start_col = start_row, start_col
        self._rng: Generator = np.random.default_rng(seed)

        self.board: NDArray[np.int8] = np.zeros(shape=(rows, cols), dtype=np.int8)
        self.mask: NDArray[np.bool] = np.zeros(shape=(rows, cols), dtype=bool)

        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self) -> None:
        all_indexes = np.arange(self.rows * self.cols)
        safe_index = self.start_row * self.cols + self.start_col
        valid_indexes = all_indexes[all_indexes != safe_index]

        sample_indexes: NDArray[np.int64] = self._rng.choice(a=valid_indexes, size=self.amount_mines, replace=False)

        mine_rows = sample_indexes // self.cols
        mine_cols = sample_indexes % self.cols
        self.board[mine_rows, mine_cols] = -1

    def _calculate_numbers(self):
        mine_mask: NDArray[np.bool] = self.board == -1

        kernel = np.ones((3, 3), dtype=np.int8)
        kernel[1, 1] = 0

        padded = np.pad(array=mine_mask, pad_width=1, mode="constant", constant_values=False)

        for i in range(self.rows):
            for j in range(self.cols):
                if not mine_mask[i, j]:
                    self.board[i, j] = np.sum(padded[i:i + 3, j:j + 3] * kernel)

    def _get_neighbors(self, row: int, col: int) -> NDArray[np.int64]:
        offsets = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]])

        neighbors = np.array([row, col]) + offsets
        valid = (neighbors[:, 0] >= 0) & (neighbors[:, 0] < self.rows) & (neighbors[:, 1] >= 0) & (
                neighbors[:, 1] < self.cols)

        valid_neighbors = neighbors[valid]
        return valid_neighbors

    def open_cell(self, row: int, col: int) -> int:
        if self.board[row, col] == -1:
            return 0
        elif self.board[row, col] == 0:
            return self._expand(row, col)
        else:
            self.mask[row, col] = True
            return 1

    def _expand(self, row: int, col: int) -> int:
        queue = [(row, col)]
        visited = np.zeros(shape=(self.rows, self.cols), dtype=bool)
        visited[row, col] = True
        num_opened_cells = 0

        while queue:
            row, col = queue.pop()

            if self.mask[row, col]:
                continue

            self.mask[row, col] = True
            num_opened_cells += 1

            if self.board[row, col] == 0:
                neighbors = self._get_neighbors(row, col)

                for neighbor_row, neighbor_col in neighbors:
                    if not visited[neighbor_row, neighbor_col] and not self.mask[neighbor_row, neighbor_col]:
                        visited[neighbor_row, neighbor_col] = True
                        queue.append((neighbor_row, neighbor_col))

        return num_opened_cells

    def get_state(self) -> NDArray[np.int8]:
        state = np.full(shape=(self.rows, self.cols), fill_value=-2, dtype=np.int8)
        state[self.mask] = self.board[self.mask]
        return state

    def __repr__(self):
        return f"Minesweeper(rows={self.rows}, cols={self.cols}, amount_mines={self.amount_mines}, start_row={self.start_row}, start_col={self.start_col})"

    def __str__(self):
        self.open_cell(0, 0)
        state = self.get_state()
        board_str = []
        for row in state:
            row_str = []
            for cell in row:
                if cell == -2:
                    row_str.append(" ")
                elif cell == 0:
                    row_str.append("0")
                else:
                    row_str.append(cell)
            board_str.append(row_str)

        board_str = tabulate(board_str, tablefmt="double_grid")
        return board_str
