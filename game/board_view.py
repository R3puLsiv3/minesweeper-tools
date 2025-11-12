import pygame
from pygame import Surface
import pygame_gui


class BoardView(Surface):

    def __init__(self, board_width, board_height):
        self.cell_width = 30
        self.cell_height = 30
        screen_size = (board_width * self.cell_width, board_height * self.cell_height)
        self.screen = super().__init__(size=screen_size)
        self.board_width = board_width
        self.board_height = board_height

    def draw_board(self, manager):
        for i in range(self.board_height):
            for j in range(self.board_width):
                pygame.draw.rect(self, (64, 64, 64),
                                 (j * self.cell_width, i * self.cell_height, self.cell_width, self.cell_height))
