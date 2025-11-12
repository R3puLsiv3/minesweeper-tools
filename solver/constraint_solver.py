import numpy as np
import cpmpy as cp
from numpy.typing import NDArray


class Solver:
    def __init__(self, board: NDArray[np.int8], border: set[int, int] = None):
        self.border = border
        self.board = board
        self.model = cp.Model()

        self.init_constraints()

    def init_constraints(self):
        pass

    def update_constraints(self):
        pass

    def step(self):
        pass
