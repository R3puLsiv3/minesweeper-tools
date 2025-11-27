import pygame
from sys import exit

import pygame_gui
from pygame import Surface
from pygame.time import Clock
from board_view import BoardView, CellTypes
from board_model import BoardModel, CellModel
from board_generation import BoardTypes
from config import BOARD_BORDER


class Minesweeper:

    def __init__(self) -> None:
        pygame.init()
        self.name = "Minesweeper"
        self.screen = None

        self.clock: Clock = pygame.time.Clock()
        self.__tick_rate = 200

        self.board_model = BoardModel(9, 9, 10, BoardTypes.OPENED, start_cell=(0, 0))
        self.board_view = BoardView(9, 9)

        self.width = min(self.board_view.width + 200, pygame.display.Info().current_w)
        self.height = min(self.board_view.height + 100, pygame.display.Info().current_h)

        self.manager = pygame_gui.UIManager((self.width, self.height))

        self.pushed_cells = []

        self.text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 100), (50, 30)),
                                                              manager=self.manager, object_id="#main_text_entry")

    def run(self) -> None:
        pygame.display.set_caption(self.name)
        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))
        self.board_view.set_position(self.screen.width - self.board_view.width - BOARD_BORDER, BOARD_BORDER)
        self.screen.fill(color="gray30")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.manager.process_events(event)

                self.__handle_pushed_cells()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if event.button == 3 and self.board_view.clicked_cell(x_pos, y_pos):
                        x, y = self.board_view.get_cell(x_pos, y_pos)
                        self.flag_cell(x, y)

                if event.type == pygame.MOUSEBUTTONUP:
                    x_pos, y_pos = event.pos
                    if event.button == 1 and self.board_view.clicked_cell(x_pos, y_pos):
                        x, y = self.board_view.get_cell(x_pos, y_pos)
                        if not self.board_model.is_flagged(x, y):
                            self.open_cell(x, y)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_board(0, 0)

            self.board_view.draw(self.screen)

            self.manager.update(self.clock.tick(self.__tick_rate) / 1000)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
            self.clock.tick(self.__tick_rate)

    def __handle_pushed_cells(self) -> None:
        x_pos, y_pos = pygame.mouse.get_pos()
        if self.board_view.clicked_cell(x_pos, y_pos) and pygame.mouse.get_pressed()[0]:
            self.__reset_cells()
            x, y = self.board_view.get_cell(x_pos, y_pos)
            if not self.board_model.is_flagged(x, y) and not self.board_model.is_revealed(x, y):
                self.__push_cell(x, y)
            if self.board_model.is_revealed(x, y) and self.board_model.get_value(x, y):
                for neighbor in self.board_model.get_neighbors(x, y):
                    if (not self.board_model.is_revealed(neighbor.x, neighbor.y)
                            and not self.board_model.is_flagged(neighbor.x, neighbor.y)):
                        self.__push_cell(neighbor.x, neighbor.y)
        elif self.pushed_cells:
            self.__reset_cells()

    def __push_cell(self, x: int, y: int) -> None:
        self.pushed_cells.append((x, y))
        self.board_view.draw_pushed(x, y)

    def __reset_cells(self) -> None:
        for x, y in self.pushed_cells:
            self.board_view.draw_empty(x, y)
            self.pushed_cells = []

    def open_cell(self, x: int, y: int) -> None:
        if (opening := self.board_model.open(x, y)) is None:
            # If a mine is opened on the first try, create a new board with the start cell at that position.
            if not self.board_model.is_opened():
                # Keep already placed flags on the board.
                if self.board_model.mine_counter != self.board_model.get_amount_mines():
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
                self.board_view.draw_cells(number_cell_models)
                self.board_view.draw_cells(mine_cell_models, CellTypes.CELL_MINE)
                self.board_view.draw_cells(false_flag_cell_models, CellTypes.CELL_FALSE_FLAG)
        else:
            self.board_view.draw_cells(opening)
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
        self.board_view.set_position(self.screen.width - self.board_view.width - BOARD_BORDER, BOARD_BORDER)


def main() -> None:
    game = Minesweeper()
    game.run()


if __name__ == "__main__":
    main()
