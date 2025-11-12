from board_generation.board import Board
import random


class NoGuessBoard(Board):

    def __init__(self, width: int, height: int, amount_mines: int, start_cell: tuple[int, int]):
        super().__init__(width=width, height=height, amount_mines=amount_mines)
        self.start_cell: tuple[int, int] = start_cell
        self.start_row, self.start_col = self.start_cell

        self.grid = []
        self.mine_probability = self.amount_mines / self.amount_cells

        self.wave_function_collapse()

    class Cell:

        def __init__(self, x: int, y: int, options: list[int], weights: list[int]):
            self.x: int = x
            self.y: int = y
            self.options: list[int] = options
            self.weights: list[int] = weights
            self.collapsed: bool = False

        def entropy(self):
            return len(self.options)

        def observe(self):
            random.choices(population=self.options, weights=self.weights)

    def wave_function_collapse(self):
        self.initialize_grid()

    def initialize_grid(self):
        pass
