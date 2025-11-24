import pygame
from sys import exit
from pygame import Surface
from pygame.time import Clock
from board_view import BoardView
from board_model import BoardModel
from board_generation import BoardTypes


class Minesweeper:

    def __init__(self) -> None:
        pygame.init()
        self.name = "Minesweeper"
        self.screen = None

        self.clock: Clock = pygame.time.Clock()
        self.__tick_rate = 100

        self.board_model = BoardModel(5, 5, 3, BoardTypes.CLOSED)
        self.board_view = BoardView(5, 5)
        self.width = self.board_view.width
        self.height = self.board_view.height

        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))

    def run(self) -> None:
        pygame.display.set_caption(self.name)
        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = get_cell_index(event.pos)
                    # self.board_view.draw_cell_pushed(x, y)

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = get_cell_index(event.pos)
                    if event.button == 1:
                        if opening := self.board_model.open(x, y):
                            self.board_view.draw_opening(opening)
                            if self.board_model.finished():
                                pass
                    if event.button == 3:
                        if self.board_model.is_flagged(x, y):
                            self.board_model.set_empty(x, y)
                            self.board_view.draw_empty(x, y)
                        else:
                            self.board_model.set_flag(x, y)
                            self.board_view.draw_flag(x, y)

            self.screen.blit(self.board_view)

            pygame.display.update()
            self.clock.tick(self.__tick_rate)


def get_cell_index(event_pos: tuple[int, int]):
    x, y = event_pos
    return x // 32, y // 32


game = Minesweeper()
game.run()
