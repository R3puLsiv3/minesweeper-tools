import numpy as np


class Board:
    def __init__(self, size: tuple[int, int], amount_mines: int, no_guess: bool = False):
        self.size = size
        (self.width, self.height) = self.size
        self.amount_cells = self.width * self.height
        self.amount_mines = min(amount_mines, self.amount_cells)
        self.no_guess = no_guess
        self.board = np.zeros(shape=(self.height, self.width), dtype=int)

        if no_guess:
            self.generate_no_guess_board(self.amount_mines)
        else:
            self.generate_standard_board(self.amount_mines)


    def generate_standard_board(self):
