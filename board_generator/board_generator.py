import numpy as np
import random


class Board:
    MAX_LENGTH: int = 100

    def __init__(self, size: tuple[int, int], amount_mines: int, no_guess: bool = False,
                 opening: tuple[int, int] = None) -> None:
        self.size = (min(size[0], self.MAX_LENGTH), min(size[1], self.MAX_LENGTH))
        self.width, self.height = self.size
        self.amount_cells = self.width * self.height
        self.amount_mines = min(amount_mines, self.amount_cells - 1)
        self.mine_indexes = []
        self.no_guess = no_guess
        self.opening = opening
        self.board = np.zeros(shape=(self.height, self.width), dtype=int)

        if no_guess:
            self.generate_no_guess_board()
        else:
            self.generate_standard_board()

    def generate_standard_board(self) -> None:
        """
        Places the mines and calculates the values of the numbers on the board.
        """
        self.place_mines()
        print(self.board)
        self.adjust_numbers()
        print(self.board)

    def place_mines(self) -> None:
        """
        Chooses mine positions of the required amount by sampling randomly from a uniform distribution and places the
        mines on the board at those positions.
        """
        sample = random.sample(population=range(0, self.amount_cells), k=self.amount_mines)
        for num in sample:
            index = (num // self.height, num % self.width)
            self.board[index] = -1
            self.mine_indexes.append(index)

    def adjust_numbers(self) -> None:
        """
        Adjusts the numbers next to mines to the amount of mines they touch.
        """
        offsets = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for (row, col) in self.mine_indexes:
            for (row_offset, col_offset) in offsets:
                (neighbor_row, neighbor_col) = (row + row_offset, col + col_offset)
                if (0 <= neighbor_row < self.height and 0 <= neighbor_col < self.width
                        and self.board[neighbor_row, neighbor_col] != -1):
                    self.board[neighbor_row, neighbor_col] += 1

    def generate_no_guess_board(self) -> None:
        pass


board = Board((3, 3), 2, opening=(0, 0))
