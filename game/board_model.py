from board_generation import generate_board, BoardTypes, Cell
from config import OFFSETS


class BoardModel:

    def __init__(self, width: int, height: int, amount_mines: int, board_type: BoardTypes, start_cell: tuple[int, int]):
        self.__board = generate_board(width=width, height=height, amount_mines=amount_mines, board_type=board_type,
                                      start_cell=start_cell)
        self.width: int = width
        self.height: int = height
        self.amount_mines: int = self.__board.amount_mines
        self.cells_to_open: int = self.__board.amount_cells - self.amount_mines

    def set_flag(self, x: int, y: int) -> None:
        self.__board.get_cell(x, y).flagged = True
        self.amount_mines -= 1

    def remove_flag(self, x: int, y: int) -> None:
        self.__board.get_cell(x, y).flagged = False
        self.amount_mines += 1

    def is_flagged(self, x: int, y: int) -> bool:
        return self.__board.get_cell(x, y).flagged

    def is_revealed(self, x: int, y: int) -> bool:
        return self.__board.get_cell(x, y).revealed

    def finished(self) -> bool:
        return self.cells_to_open == 0

    def open(self, x: int, y: int) -> None | set[Cell]:
        cell = self.__board.get_cell(x, y)
        if cell.is_mine:
            return None
        if cell.value == 0:
            return self.__expand(cell)
        else:
            cell.revealed = True
            self.cells_to_open -= 1
            return {cell}

    def __expand(self, cell: Cell) -> set[Cell]:
        queue = [cell]
        opening: set[Cell] = set()
        while queue:
            cell = queue.pop()
            cell.revealed = True
            self.cells_to_open -= 1
            opening.add(cell)
            for x_offset, y_offset in OFFSETS:
                neighbor_x, neighbor_y = cell.x + x_offset, cell.y + y_offset
                if ((neighbor_x, neighbor_y) not in opening and 0 <= neighbor_x < self.__board.height
                        and 0 <= neighbor_y < self.__board.width):
                    neighbor_cell = self.__board.get_cell(neighbor_x, neighbor_y)
                    if neighbor_cell.is_mine:
                        continue
                    if neighbor_cell.value == 0:
                        queue.append(neighbor_cell)
                    else:
                        opening.add(neighbor_cell)
        return opening
