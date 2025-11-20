from board_generation.board import Board


class NoGuessBoard(Board):
    """
    This class requires the implementation of a solver.
    """
    def __init__(self, width: int, height: int, amount_mines: int, start_cell: tuple[int, int]):
        super().__init__(width=width, height=height)
        self.start_cell: tuple[int, int] = start_cell
        self.start_x, self.start_y = self.start_cell
        self.__place_mines(amount_mines)

    def __place_mines(self, amount_mines: int) -> None:
        raise NotImplementedError
