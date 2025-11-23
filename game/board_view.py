import pygame
from pygame import Surface
from game import NumberCell


class Cell(pygame.sprite.Sprite):

    def __init__(self, sprite: Surface):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect()


class BoardView(Surface):

    def __init__(self, board_width, board_height):
        self.cell_length = pygame.image.load("sprites/cell_0.png").width
        screen_size = (board_width * self.cell_length, board_height * self.cell_length)
        self.screen = super().__init__(size=screen_size)
        self.board_width = board_width
        self.board_height = board_height
        self.__load_sprites()
        self.__value_sprites = {0: self.spr_cell_0, 1: self.spr_cell_1, 2: self.spr_cell_2, 3: self.spr_cell_3,
                                4: self.spr_cell_4, 5: self.spr_cell_5, 6: self.spr_cell_6,
                                7: self.spr_cell_7, 8: self.spr_cell_8, 9: self.spr_cell_empty}
        # TODO: Create enum to access values_sprite
        self.__draw_board()

    def __draw_board(self):
        for x in range(self.board_height):
            for y in range(self.board_width):
                self.blit(self.spr_cell_empty, (x * self.cell_length, y * self.cell_length))

    def draw_opening(self, number_cells: list[NumberCell]) -> None:
        for cell in number_cells:
            self.blit(self.__value_sprites[cell.value], dest=(cell.x * self.cell_length, cell.y * self.cell_length))

    # TODO: Return group of sprite(s) to update

    def draw_cell_pushed(self, x: int, y: int) -> None:
        self.blit(self.__value_sprites[8], dest=(x * self.cell_length, y * self.cell_length))

    def __load_sprites(self):
        self.spr_cell_0 = pygame.image.load("sprites/cell_0.png").convert(self)
        self.spr_cell_1 = pygame.image.load("sprites/cell_1.png").convert(self)
        self.spr_cell_2 = pygame.image.load("sprites/cell_2.png").convert(self)
        self.spr_cell_3 = pygame.image.load("sprites/cell_3.png").convert(self)
        self.spr_cell_4 = pygame.image.load("sprites/cell_4.png").convert(self)
        self.spr_cell_5 = pygame.image.load("sprites/cell_5.png").convert(self)
        self.spr_cell_6 = pygame.image.load("sprites/cell_6.png").convert(self)
        self.spr_cell_7 = pygame.image.load("sprites/cell_7.png").convert(self)
        self.spr_cell_8 = pygame.image.load("sprites/cell_8.png").convert(self)
        self.spr_mine = pygame.image.load("sprites/cell_mine.png").convert(self)
        self.spr_cell_empty = pygame.image.load("sprites/cell_empty.png").convert(self)
        self.spr_cell_flag = pygame.image.load("sprites/cell_flag.png").convert(self)
        self.spr_mine_explosion = pygame.image.load("sprites/cell_mine_explosion.png").convert(self)
        self.spr_mine_false = pygame.image.load("sprites/tile_mine_false.png").convert(self)
