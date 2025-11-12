import pygame
from sys import exit
from pygame import Surface
from pygame.time import Clock
import pygame_gui
from board_view import BoardView
from options_view import OptionsView


class Minesweeper:

    def __init__(self):
        pygame.init()
        self.name = "Minesweeper"
        self.screen = None

        self.clock: Clock = pygame.time.Clock()
        self.__TICK_RATE = 60

        self.board_view = BoardView(9, 9)
        self.width = self.board_view.width
        self.height = self.board_view.height + 105
        self.manager = pygame_gui.UIManager((self.width, self.height), theme_path="theme.json")

        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))
        self.width_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 30), (50, 30)),

                                                               manager=self.manager, object_id="width_input")

        self.height_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((90, 30), (50, 30)),
                                                                manager=self.manager, object_id="height_input")
        self.create_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 30), (50, 30)),
                                                          manager=self.manager, object_id="create_button",
                                                          text="Go")

        self.spr_grid_tile_empty = pygame.image.load("sprites/tile_empty.png").convert(self.board_view)
        self.spr_tile_flag = pygame.image.load("sprites/tile_flag.png").convert(self.board_view)
        self.spr_tile_0 = pygame.image.load("sprites/tile_0.png").convert(self.board_view)
        self.spr_tile_1 = pygame.image.load("sprites/tile_1.png").convert(self.board_view)
        self.spr_tile_2 = pygame.image.load("sprites/tile_2.png").convert(self.board_view)
        self.spr_tile_3 = pygame.image.load("sprites/tile_3.png").convert(self.board_view)
        self.spr_tile_4 = pygame.image.load("sprites/tile_4.png").convert(self.board_view)
        self.spr_tile_5 = pygame.image.load("sprites/tile_5.png").convert(self.board_view)
        self.spr_tile_6 = pygame.image.load("sprites/tile_6.png").convert(self.board_view)
        self.spr_tile_7 = pygame.image.load("sprites/tile_7.png").convert(self.board_view)
        self.spr_tile_8 = pygame.image.load("sprites/tile_8.png").convert(self.board_view)
        self.spr_mine = pygame.image.load("sprites/tile_mine.png").convert(self.board_view)
        self.spr_mine_clicked = pygame.image.load("sprites/tile_mine_exploded.png").convert(self.board_view)
        self.spr_mine_false = pygame.image.load("sprites/tile_mine_wrong.png").convert(self.board_view)

    def run(self):
        pygame.display.set_caption(self.name)
        self.screen: Surface = pygame.display.set_mode(size=(self.width, self.height))
        self.board_view.draw_board(self.manager)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)

                if event.type == pygame.MOUSEBUTTONUP:
                    pass

                self.manager.process_events(event)

            self.manager.update(self.clock.tick(self.__TICK_RATE))

            self.manager.draw_ui(self.screen)

            self.screen.blit(self.board_view, (self.width / 2 - self.board_view.width / 2, 0))

            pygame.display.update()


game = Minesweeper()
game.run()
