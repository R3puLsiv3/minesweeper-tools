from dataclasses import dataclass

from board_generation import generate_board, BoardTypes, Cell, Board


@dataclass
class CellModel:
    x: int
    y: int
    value: int | None


class BoardModel:

    def __init__(self, width: int, height: int, amount_mines: int, board_type: BoardTypes = BoardTypes.OPENED,
                 start_cell: tuple[int, int] = (0, 0)) -> None:
        self.__board: Board = generate_board(width=width, height=height, amount_mines=amount_mines,
                                             board_type=board_type,
                                             start_cell=start_cell)
        self.width: int = width
        self.height: int = height
        self.mines_to_flag: int = self.__board.amount_mines
        self.cells_to_open: int = self.__board.amount_cells - self.mines_to_flag
        self.faulty_cell_model: CellModel | None = None

    def set_flag(self, x: int, y: int) -> None:
        self.__board.get_cell(x, y).flagged = True
        self.mines_to_flag -= 1

    def set_empty(self, x: int, y: int) -> None:
        self.__board.get_cell(x, y).flagged = False
        self.mines_to_flag += 1

    def is_flagged(self, x: int, y: int) -> bool:
        return self.__board.get_cell(x, y).flagged

    def is_revealed(self, x: int, y: int) -> bool:
        return self.__board.get_cell(x, y).revealed

    def is_opened(self) -> bool:
        return self.cells_to_open != self.__board.amount_cells - self.mines_to_flag

    def get_value(self, x: int, y: int) -> int:
        return self.__board.get_cell(x, y).value

    def get_flagged(self) -> list[CellModel]:
        return [CellModel(x, y, None) for x in range(self.width) for y in range(self.height) if
                self.__board.get_cell(x, y).flagged]

    def get_amount_mines(self) -> int:
        return self.__board.amount_mines

    def finished(self) -> bool:
        return self.cells_to_open == 0

    def open(self, x: int, y: int) -> None | list[CellModel]:
        cell: Cell = self.__board.get_cell(x, y)
        if cell.revealed:
            return self.chord(x, y)
        if cell.is_mine:
            cell.revealed = True
            self.faulty_cell_model = CellModel(cell.x, cell.y, None)
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

    def chord(self, x: int, y: int) -> None | list[CellModel]:
        cell: Cell = self.__board.get_cell(x, y)
        neighbor_cells: list[Cell] = []
        amount_flags = 0
        false_flag = False
        for neighbor_cell in self.__board.get_neighbors(cell):
            if neighbor_cell.flagged:
                amount_flags += 1
                if not neighbor_cell.is_mine:
                    self.faulty_cell_model = CellModel(neighbor_cell.x, neighbor_cell.y, None)
                    false_flag = True
            elif not neighbor_cell.revealed:
                neighbor_cells.append(neighbor_cell)
        opening: list[CellModel] = []
        if amount_flags == cell.value:
            if false_flag:
                self.__board.get_cell(self.faulty_cell_model.x, self.faulty_cell_model.y).revealed = True
                return None
            for neighbor_cell in neighbor_cells:
                opening += self.open(neighbor_cell.x, neighbor_cell.y)
        return opening

    def open_all(self) -> tuple[list[CellModel], list[CellModel], list[CellModel]]:
        number_cell_models = []
        mine_cell_models = []
        false_flag_cell_models = []
        for x in range(self.width):
            for y in range(self.height):
                current_cell = self.__board.get_cell(x, y)
                if current_cell.revealed:
                    continue
                if current_cell.is_mine:
                    mine_cell_models.append(CellModel(x, y, None))
                    current_cell.revealed = True
                elif current_cell.flagged:
                    false_flag_cell_models.append(CellModel(x, y, None))
                else:
                    number_cell_models.append(CellModel(x, y, current_cell.value))
        return number_cell_models, mine_cell_models, false_flag_cell_models
