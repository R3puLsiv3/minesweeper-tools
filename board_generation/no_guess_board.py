from board import Board


class NoGuessBoard(Board):

    def __init__(self, size: tuple[int, int], amount_mines: int, start_cell: tuple[int, int]):
        super().__init__(size=size, amount_mines=amount_mines)
        self.start_cell: tuple[int, int] = start_cell
        self.start_row, self.start_col = self.start_cell
