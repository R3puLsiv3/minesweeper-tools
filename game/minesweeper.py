import pygame
from sys import exit

import pygame_gui
from pygame import Surface
from pygame.time import Clock
from game.board_view import BoardView, CellTypes
from game.board_model import BoardModel, CellModel
from game.options_view import OptionsView
from config import PADDING, OPTIONS_WIDTH, OPTIONS_HEIGHT, BOARD_X, BOARD_Y, CELL_LENGTH


class Minesweeper:

    def __init__(self, board_width=9, board_height=9, amount_mines=10) -> None:
        pygame.init()
        self.name = "Minesweeper"
        self.screen = None

        self.clock: Clock = pygame.time.Clock()
        self.__tick_rate = 200

        self.board_model = BoardModel(board_width, board_height, amount_mines, start_cell=(0, 0))
        board_view_width, board_view_height = board_width * CELL_LENGTH, board_height * CELL_LENGTH
        self.board_view = BoardView(board_view_width, board_view_height)
        self.options_view = None

        self.width = BOARD_X + self.board_view.width + PADDING
        self.height = BOARD_Y + self.board_view.height + PADDING

        self.pushed_cells = []

    def run(self) -> None:

        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))
        pygame.display.set_caption(self.name)
        self.options_view = OptionsView(OPTIONS_WIDTH, OPTIONS_HEIGHT, self.board_view.board_width,
                                        self.board_view.board_height, self.board_model.get_amount_mines(),
                                        pygame_gui.UIManager((self.width, self.height)))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.options_view.options_manager.process_events(event)

                self.__handle_pushed_cells()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if event.button == 3 and self.board_view.clicked_cell(x_pos, y_pos):
                        x, y = self.board_view.get_cell(x_pos, y_pos)
                        self.flag_cell(x, y)
                        self.options_view.update_mine_counter(self.board_model.mine_counter)

                if event.type == pygame.MOUSEBUTTONUP:
                    x_pos, y_pos = event.pos
                    if event.button == 1 and self.board_view.clicked_cell(x_pos, y_pos):
                        x, y = self.board_view.get_cell(x_pos, y_pos)
                        if not self.board_model.is_flagged(x, y):
                            self.open_cell(x, y)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_board(self.board_model.width, self.board_model.height,
                                         self.board_model.get_amount_mines())

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    width, height, amount_mines = self.options_view.get_board_data()
                    self.reset_board(width, height, amount_mines)

            self.screen.fill(color="gray30")

            self.board_view.draw(self.screen)

            self.options_view.options_manager.update(self.clock.tick(self.__tick_rate) / 1000)
            self.options_view.draw(self.screen)

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
                    self.board_model = BoardModel(self.board_model.width, self.board_model.height,
                                                  self.board_model.get_amount_mines(), (x, y))
                    for cell_model in flagged_cell_models:
                        self.board_model.set_flag(cell_model.x, cell_model.y)
                else:
                    self.board_model = BoardModel(self.board_model.width, self.board_model.height,
                                                  self.board_model.get_amount_mines(), (x, y))
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
                self.board_model.reset_flag(x, y)
                self.board_view.draw_empty(x, y)
            else:
                self.board_model.set_flag(x, y)
                self.board_view.draw_flag(x, y)

    def check_finished(self) -> None:
        if self.board_model.finished():
            _, mine_cell_models, _ = self.board_model.open_all()
            for mine_cell_model in mine_cell_models:
                self.board_view.draw_flag(mine_cell_model.x, mine_cell_model.y)
        self.options_view.update_mine_counter(self.board_model.mine_counter)

    def reset_board(self, board_width, board_height, amount_mines, start_cell=(0, 0)) -> None:
        self.board_model = BoardModel(board_width, board_height, amount_mines, start_cell)
        board_view_width, board_view_height = board_width * CELL_LENGTH, board_height * CELL_LENGTH
        self.board_view = BoardView(board_view_width, board_view_height)
        self.width = BOARD_X + self.board_view.width + PADDING
        self.height = BOARD_Y + self.board_view.height + PADDING
        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))
        self.options_view.update_mine_counter(self.board_model.mine_counter)


def main() -> None:
    game = Minesweeper()
    game.run()


if __name__ == "__main__":
    main()
