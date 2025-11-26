import pygame
from sys import exit
from pygame import Surface
from pygame.time import Clock
from board_view import BoardView, CellTypes
from board_model import BoardModel, CellModel
from board_generation import BoardTypes
from config import OFFSETS


class Minesweeper:

    def __init__(self) -> None:
        pygame.init()
        self.name = "Minesweeper"
        self.screen = None

        self.clock: Clock = pygame.time.Clock()
        self.__tick_rate = 200

        self.board_model = BoardModel(9, 9, 10, BoardTypes.OPENED, start_cell=(0, 0))
        self.board_view = BoardView(9, 9)
        self.width = self.board_view.width
        self.height = self.board_view.height
        self.pushed_cell = None
        self.chord_pushed_cells = []

    def run(self) -> None:
        pygame.display.set_caption(self.name)
        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.__handle_pushed_cells()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = get_cell_index(event.pos)
                    if event.button == 3:
                        self.flag_cell(x, y)

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = get_cell_index(event.pos)
                    if event.button == 1 and self.board_view.get_rect().collidepoint(
                            event.pos) and not self.board_model.is_flagged(x, y):
                        self.open_cell(x, y)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_board(0, 0)

            self.screen.blit(self.board_view)

            pygame.display.update()
            self.clock.tick(self.__tick_rate)

    def __handle_pushed_cells(self) -> None:
        x, y = pygame.mouse.get_pos()
        if self.board_view.get_rect().collidepoint(x, y) and pygame.mouse.get_pressed()[0]:
            x, y = get_cell_index((x, y))
            # If a previously pushed cell exists, check if another cell is pushed and reset the previously pushed cells.
            if self.pushed_cell:
                old_x, old_y = self.pushed_cell
                # A new cell is being pushed.
                if (x, y) != (old_x, old_y):
                    self.board_view.draw_empty(old_x, old_y)
                    self.pushed_cell = None
                # The same cell is being pushed.
                else:
                    return
            if self.chord_pushed_cells:
                for neighbor_x, neighbor_y in self.chord_pushed_cells:
                    self.board_view.draw_empty(neighbor_x, neighbor_y)
                self.chord_pushed_cells = []
            # If an empty cell is pushed, set it to pushed.
            if not self.board_model.is_flagged(x, y) and not self.board_model.is_revealed(x, y):
                self.pushed_cell = (x, y)
                self.board_view.draw_pushed(x, y)
            # If a number cell is pushed set the empty neighbors to pushed.
            if self.board_model.is_revealed(x, y) and self.board_model.get_value(x, y):
                for x_offset, y_offset in OFFSETS:
                    neighbor_x, neighbor_y = x + x_offset, y + y_offset
                    if 0 <= neighbor_x < self.board_model.width and 0 <= neighbor_y < self.board_model.height:
                        if not self.board_model.is_revealed(neighbor_x,
                                                            neighbor_y) and not self.board_model.is_flagged(
                            neighbor_x, neighbor_y):
                            self.chord_pushed_cells.append((neighbor_x, neighbor_y))
                            self.board_view.draw_pushed(neighbor_x, neighbor_y)
        # If no cell is pushed, reset the previously pushed cells.
        else:
            if self.pushed_cell:
                x, y = self.pushed_cell
                self.board_view.draw_empty(x, y)
                self.pushed_cell = None
            if self.chord_pushed_cells:
                for neighbor_x, neighbor_y in self.chord_pushed_cells:
                    self.board_view.draw_empty(neighbor_x, neighbor_y)
                self.chord_pushed_cells = []

    def open_cell(self, x: int, y: int) -> None:
        if (opening := self.board_model.open(x, y)) is None:
            # If a mine is opened on the first try, create a new board with the start cell at that position.
            if not self.board_model.is_opened():
                # Keep already placed flags on the board.
                if self.board_model.mines_to_flag == self.board_model.get_amount_mines():
                    flagged_cell_models = self.board_model.get_flagged()
                    self.board_model = BoardModel(9, 9, 10, BoardTypes.OPENED, (x, y))
                    for cell_model in flagged_cell_models:
                        self.board_model.set_flag(cell_model.x, cell_model.y)
                else:
                    self.board_model = BoardModel(9, 9, 10, BoardTypes.OPENED, (x, y))
                # Open the now guaranteed safe cell.
                self.open_cell(x, y)
                self.check_finished()
            # If it was not the first try, reveal the entire board as the game is lost.
            else:
                number_cell_models, mine_cell_models, false_flag_cell_models = self.board_model.open_all()
                faulty_cell_model = self.board_model.faulty_cell_model
                self.board_view.draw_mine_explosion(faulty_cell_model.x, faulty_cell_model.y)
                self.board_view.draw(number_cell_models)
                self.board_view.draw(mine_cell_models, CellTypes.CELL_MINE)
                self.board_view.draw(false_flag_cell_models, CellTypes.CELL_MINE_FALSE)
        else:
            self.board_view.draw(opening)
            self.check_finished()

    def flag_cell(self, x: int, y: int) -> None:
        if not self.board_model.is_revealed(x, y):
            if self.board_model.is_flagged(x, y):
                self.board_model.set_empty(x, y)
                self.board_view.draw_empty(x, y)
            else:
                self.board_model.set_flag(x, y)
                self.board_view.draw_flag(x, y)

    def check_finished(self) -> None:
        if self.board_model.finished():
            _, mine_cell_models, _ = self.board_model.open_all()
            for mine_cell_model in mine_cell_models:
                self.board_view.draw_flag(mine_cell_model.x, mine_cell_model.y)

    def reset_board(self, x: int, y: int) -> None:
        self.board_model = BoardModel(9, 9, 10, BoardTypes.OPENED, (x, y))
        self.board_view = BoardView(9, 9)


def get_cell_index(event_pos: tuple[int, int]):
    x, y = event_pos
    return x // 32, y // 32


def main() -> None:
    game = Minesweeper()
    game.run()


if __name__ == "__main__":
    main()
