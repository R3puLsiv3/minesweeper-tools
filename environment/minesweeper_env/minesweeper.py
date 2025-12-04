from numpy.random import Generator
import numpy as np
from numpy.typing import NDArray


class Minesweeper:

    def __init__(self, width, height, amount_mines):
        self.width = width
        self.height = height
        self.amount_cells = self.width * self.height
        self.amount_mines = amount_mines
        self.neighbors = None
        self.board = None
        self.revealed = None
        self._rng: Generator = np.random.default_rng()
        self._set_neighbors()

    def _set_neighbors(self):
        self.neighbors = [[] for _ in range(self.amount_cells)]

        for i in range(self.amount_cells):
            # Upper neighbor.
            upper_neighbor = i - self.width
            if upper_neighbor >= 0:
                self.neighbors[i].append(upper_neighbor)
            else:
                upper_neighbor = None

            # Lower neighbor.
            lower_neighbor = i + self.width
            if lower_neighbor < self.amount_cells:
                self.neighbors[i].append(lower_neighbor)
            else:
                lower_neighbor = None

            # Left neighbor.
            if i % self.width != 0:
                self.neighbors[i].append(i - 1)
                # Upper-left neighbor.
                if upper_neighbor is not None:
                    self.neighbors[i].append(upper_neighbor - 1)
                # Lower-left neighbor.
                if lower_neighbor is not None:
                    self.neighbors[i].append(lower_neighbor - 1)

            # Right neighbor.
            if i % self.width != self.width - 1:
                self.neighbors[i].append(i + 1)
                # Upper-right neighbor.
                if upper_neighbor is not None:
                    self.neighbors[i].append(upper_neighbor + 1)
                # Lower-right neighbor.
                if lower_neighbor is not None:
                    self.neighbors[i].append(lower_neighbor + 1)

    def reset_board(self):
        self.revealed = set()
        sample: NDArray[np.int64] = self._rng.choice(a=range(1, self.amount_cells), size=self.amount_mines,
                                                     replace=False)
        self.board = [0] * self.amount_cells
        for i in sample:
            for j in self.neighbors[i]:
                self.board[j] += 1
        for i in sample:
            self.board[i] = -1


game = Minesweeper(3, 3, 2)
game.reset_board()
print(game.board)
