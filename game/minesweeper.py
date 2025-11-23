import pygame
from sys import exit
from pygame import Surface
from pygame.time import Clock
from board_view import BoardView


class Minesweeper:

    def __init__(self):
        pygame.init()
        self.name = "Minesweeper"
        self.screen = None

        self.clock: Clock = pygame.time.Clock()
        self.__TICK_RATE = 60

        self.board_view = BoardView(9, 9)
        self.width = self.board_view.width
        self.height = self.board_view.height

        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))

    def run(self):
        pygame.display.set_caption(self.name)
        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.board_view.draw_cell_pushed(x, y)

                if event.type == pygame.MOUSEBUTTONUP:
                    pass

            self.screen.blit(self.board_view)

            pygame.display.update()


game = Minesweeper()
game.run()
