from dataclasses import dataclass

from board_generation import generate_board, BoardTypes, Cell, Board


@dataclass
class CellModel:
    x: int
    y: int
    value: int


class BoardModel:

    def __init__(self, width: int, height: int, amount_mines: int, board_type: BoardTypes = BoardTypes.OPENED,
                 start_cell: tuple[int, int] = (0, 0)) -> None:
        self.__board: Board = generate_board(width=width, height=height, amount_mines=amount_mines,
                                             board_type=board_type,
                                             start_cell=start_cell)
        self.width: int = width
        self.height: int = height
        self.amount_mines: int = self.__board.amount_mines
        self.cells_to_open: int = self.__board.amount_cells - self.amount_mines
        print(self.cells_to_open)

    def set_flag(self, x: int, y: int) -> None:
        self.__board.get_cell(x, y).flagged = True
        self.amount_mines -= 1

    def set_empty(self, x: int, y: int) -> None:
        self.__board.get_cell(x, y).flagged = False
        self.amount_mines += 1

    def is_flagged(self, x: int, y: int) -> bool:
        return self.__board.get_cell(x, y).flagged

    def is_revealed(self, x: int, y: int) -> bool:
        return self.__board.get_cell(x, y).revealed

    def finished(self) -> bool:
        print(self.cells_to_open)
        return self.cells_to_open == 0

    def open(self, x: int, y: int) -> None | list[CellModel]:
        cell: Cell = self.__board.get_cell(x, y)
        if cell.revealed:
            return self.chord(x, y)
        if cell.is_mine:
            return None
        if cell.value == 0:
            return self.__expand(cell)
        else:
            cell.revealed = True
            self.cells_to_open -= 1
            return [CellModel(cell.x, cell.y, cell.value)]

    def __expand(self, cell: Cell) -> list[CellModel]:
        queue: list[Cell] = [cell]
        cell.revealed = True
        opening: list[CellModel] = []
        while queue:
            cell: Cell = queue.pop()
            opening.append(CellModel(cell.x, cell.y, cell.value))
            for neighbor_cell in self.__board.get_neighbors(cell):
                if neighbor_cell.revealed or neighbor_cell.is_mine:
                    continue
                neighbor_cell.revealed = True
                if neighbor_cell.value == 0:
                    queue.append(neighbor_cell)
                else:
                    opening.append(CellModel(neighbor_cell.x, neighbor_cell.y, neighbor_cell.value))
                    neighbor_cell.revealed = True
        self.cells_to_open -= len(opening)
        return opening

    def chord(self, x: int, y: int) -> None | list[Cell]:
        cell: Cell = self.__board.get_cell(x, y)
        neighbor_cells: list[Cell] = []
        amount_flags = 0
        false_flag = False
        for neighbor_cell in self.__board.get_neighbors(cell):
            if neighbor_cell.flagged:
                amount_flags += 1
                if not neighbor_cell.is_mine:
                    false_flag = True
            elif not neighbor_cell.revealed:
                neighbor_cells.append(neighbor_cell)
        opening: list[Cell] = []
        if amount_flags == cell.value:
            if false_flag:
                return None
            for neighbor_cell in neighbor_cells:
                opening += self.open(neighbor_cell.x, neighbor_cell.y)
        return opening
