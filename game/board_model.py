import numpy as np
from board_generation.board_generator import generate_board, BoardTypes


class BoardModel:

    def __init__(self, width: int, height: int, amount_mines: int, start_cell: tuple[int, int]):
        self.board = generate_board(width=width, height=height, amount_mines=amount_mines, board_type=BoardTypes.OPENED,
                                    start_cell=start_cell)
        self.revealed = {}
        self.mine_clicked = False

    def is_clickable(self, row: int, col: int) -> bool:
        return (row, col) in self.revealed

    def click(self, row: int, col: int):
        number = self.board.cells[row, col]
        if number == -1:
            self.mine_clicked = True
        self.revealed[row, col] = number
        if number == 0:
            self.expand(row=row, col=col)

    def expand(self, row: int, col: int):
        offsets: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        queue = [(row, col)]
        while queue:
            row, col = queue.pop()
            for row_offset, col_offset in offsets:
                neighbor_row, neighbor_col = row + row_offset, col + col_offset
                if (0 <= neighbor_row < self.board.height and 0 <= neighbor_col < self.board.width and
                        (neighbor_row, neighbor_col) not in self.revealed):
                    number = self.board.cells[neighbor_row, neighbor_col]
                    if number != -1:
                        self.revealed[(neighbor_row, neighbor_col)] = number
                    if number == 0:
                        queue.append((neighbor_row, neighbor_col))
