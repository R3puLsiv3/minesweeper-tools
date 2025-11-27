import pygame
from pygame import Surface
from board_model import CellModel
from enum import IntEnum
from pygame.transform import scale
from config import CELL_LENGTH
from config import BOARD_BORDER


class CellTypes(IntEnum):
    CELL_0 = 0
    CELL_1 = 1
    CELL_2 = 2
    CELL_3 = 3
    CELL_4 = 4
    CELL_5 = 5
    CELL_6 = 6
    CELL_7 = 7
    CELL_8 = 8
    CELL_MINE = 9
    CELL_EMPTY = 10
    CELL_FLAG = 11
    CELL_MINE_EXPLOSION = 12
    CELL_FALSE_FLAG = 13


class CellView(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int, sprite: Surface) -> None:
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)


class BoardView(Surface):

    def __init__(self, board_width, board_height) -> None:
        self.cell_length = CELL_LENGTH
        screen_size = (board_width * self.cell_length, board_height * self.cell_length)
        super().__init__(size=screen_size)
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None
        self.board_width = board_width
        self.board_height = board_height
        self.__load_sprites()
        self.__sprites = self.__load_sprites()
        self.__cell_views: list[list[CellView]] = [
            [CellView(x * self.cell_length, y * self.cell_length, self.__sprites[CellTypes.CELL_EMPTY]) for x in
             range(self.board_width)] for y in range(self.board_height)]
        self.__draw_board()

    def __draw_board(self) -> None:
        for x in range(self.board_width):
            for y in range(self.board_height):
                self.get_cell_view(x, y).draw(self)

    def set_position(self, x: int, y: int):
        self.top_left = x, y
        self.top_right = x + self.width, y
        self.bottom_left = x, y + self.height
        self.bottom_right = x + self.width, y + self.height

    def clicked_cell(self, x: int, y: int) -> bool:
        x_left, y_top = self.top_left
        x_right, y_bottom = self.bottom_right
        return x_left <= x < x_right and y_top <= y < y_bottom

    def get_cell(self, x: int, y: int):
        x_left, y_top = self.top_left
        return (x - x_left) // self.cell_length, (y - y_top) // self.cell_length

    def draw(self, surface) -> None:
        surface.blit(self, dest=self.top_left)

    def draw_cells(self, cell_models: list[CellModel], cell_type: CellTypes = None) -> None:
        for cell_model in cell_models:
            cell_view = self.get_cell_view(cell_model.x, cell_model.y)
            cell_view.image = self.__sprites[cell_model.value] if cell_type is None else self.__sprites[cell_type]
            cell_view.draw(self)

    def draw_pushed(self, x: int, y: int) -> None:
        cell_view_pushed = self.get_cell_view(x, y)
        cell_view_pushed.image = self.__sprites[CellTypes.CELL_0]
        cell_view_pushed.draw(self)

    def draw_flag(self, x: int, y: int) -> None:
        cell_view_flagged = self.get_cell_view(x, y)
        cell_view_flagged.image = self.__sprites[CellTypes.CELL_FLAG]
        cell_view_flagged.draw(self)

    def draw_empty(self, x: int, y: int) -> None:
        cell_view_empty = self.get_cell_view(x, y)
        cell_view_empty.image = self.__sprites[CellTypes.CELL_EMPTY]
        cell_view_empty.draw(self)

    def draw_mine_explosion(self, x: int, y: int) -> None:
        cell_view_mine_explosion = self.get_cell_view(x, y)
        cell_view_mine_explosion.image = self.__sprites[CellTypes.CELL_MINE_EXPLOSION]
        cell_view_mine_explosion.draw(self)

    def get_cell_view(self, x: int, y: int) -> CellView:
        return self.__cell_views[y][x]

    def __load_sprites(self) -> dict[int, Surface]:
        return {CellTypes.CELL_0: scale(surface=pygame.image.load("sprites/cell_0.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_1: scale(surface=pygame.image.load("sprites/cell_1.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_2: scale(surface=pygame.image.load("sprites/cell_2.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_3: scale(surface=pygame.image.load("sprites/cell_3.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_4: scale(surface=pygame.image.load("sprites/cell_4.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_5: scale(surface=pygame.image.load("sprites/cell_5.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_6: scale(surface=pygame.image.load("sprites/cell_6.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_7: scale(surface=pygame.image.load("sprites/cell_7.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_8: scale(surface=pygame.image.load("sprites/cell_8.png").convert(self),
                                        size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_MINE: scale(surface=pygame.image.load("sprites/cell_mine.png").convert(self),
                                           size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_EMPTY: scale(surface=pygame.image.load("sprites/cell_empty.png").convert(self),
                                            size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_FLAG: scale(surface=pygame.image.load("sprites/cell_flag.png").convert(self),
                                           size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_MINE_EXPLOSION: scale(
                    surface=pygame.image.load("sprites/cell_mine_explosion.png").convert(self),
                    size=(self.cell_length, self.cell_length)),
                CellTypes.CELL_FALSE_FLAG: scale(surface=pygame.image.load("sprites/cell_false_flag.png").convert(self),
                                                 size=(self.cell_length, self.cell_length))}
