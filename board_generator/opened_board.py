from board import Board


class OpenedBoard(Board):

    def __init__(self, size: tuple[int, int], amount_mines: int, start_cell: tuple[int, int]):
        super().__init__(size=size, amount_mines=amount_mines)
        self.start_cell: tuple[int, int] = start_cell
        self.start_row, self.start_col = self.start_cell

    def generate_board(self) -> None:
        """
        Places the mines and calculates the values of the numbers on the board.
        """
        mine_indexes: list[tuple[int, int]] = self.place_mines()
        self.adjust_numbers(mine_indexes=mine_indexes)

    def place_mines(self) -> list[tuple[int, int]]:
        """
        Chooses mine positions of the required amount by sampling randomly from a uniform distribution and places the
        mines on the board at those positions while avoiding the open start cell.
        """
        low: int = self.start_row * self.height + self.start_col % self.width + 1
        high: int = low + self.amount_cells
        sample = self.rng.integers(low=low, high=high, size=self.amount_mines)
        mine_indexes: list[tuple[int, int]] = []
        for num in sample:
            index: tuple[int, int] = (num // self.height) % self.height, num % self.width
            self.board[index] = -1
            mine_indexes.append(index)
        return mine_indexes
