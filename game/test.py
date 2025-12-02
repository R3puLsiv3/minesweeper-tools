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
        self.__tick_rate = 200

        self.board_model = BoardModel(9, 9, 10, BoardTypes.OPENED, (0, 0))
        self.board_view = BoardView(9, 9)
        self.width = self.board_view.width
        self.height = self.board_view.height

        self.total_width = self.width + 200
        self.total_height = self.height + 200

        self.board_border_view = BoardBoarderView(self.width + 24, self.height + 24)

    def run(self) -> None:
        pygame.display.set_caption(self.name)
        self.screen: Surface = pygame.display.set_mode(size=(self.total_width, self.total_height))
        self.screen.fill("grey")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.blit(self.board_border_view, dest=(self.total_width - self.board_border_view.width - 50,
                                                           self.total_height - self.board_border_view.height - 50))
            self.board_border_view.blit(self.board_view, dest=(12, 12))

            pygame.display.update()
            self.clock.tick(self.__tick_rate)


class BoardBoarderView(Surface):

    def __init__(self, board_width, board_height) -> None:
        self.screen = super().__init__(size=(board_width, board_height))
        self.fill("gray30")
        self.board_width = board_width
        self.board_height = board_height
        pygame.draw.line(self, color="white", start_pos=self.get_rect().topleft, end_pos=self.get_rect().bottomleft,
                         width=10)
        pygame.draw.line(self, color="white", start_pos=self.get_rect().topleft, end_pos=self.get_rect().topright,
                         width=10)
        pygame.draw.line(self, color="black", start_pos=self.get_rect().topright, end_pos=self.get_rect().bottomright,
                         width=10)
        pygame.draw.line(self, color="black", start_pos=self.get_rect().bottomleft, end_pos=self.get_rect().bottomright,
                         width=10)


class GameView(Surface):

    def __init__(self, game_width, game_height) -> None:
        self.screen = super().__init__(size=(game_width, game_height))
        self.fill("white")
        self.board_width = game_width
        self.board_height = game_height


game = Minesweeper()
game.run()
