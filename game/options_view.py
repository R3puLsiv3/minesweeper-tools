from pygame import Surface
import pygame_gui
import pygame
from config import OPTION_WIDTH, OPTION_HEIGHT, OPTIONS_X, OPTIONS_Y, TEXT_ENTRY_WIDTH_X, TEXT_ENTRY_WIDTH_Y, \
    TEXT_ENTRY_HEIGHT_X, \
    TEXT_ENTRY_HEIGHT_Y, BUTTON_CREATE_X, BUTTON_CREATE_Y, TEXT_ENTRY_AMOUNT_MINES_X, TEXT_ENTRY_AMOUNT_MINES_Y, \
    TEXT_MINE_COUNTER_X, TEXT_MINE_COUNTER_Y


class OptionsView(Surface):

    def __init__(self, width: int, height: int, board_width, board_height, amount_mines, manager) -> None:
        super().__init__(size=(width, height))
        self.pos = (OPTIONS_X, OPTIONS_Y)
        self.options_manager = manager
        self.text_entry_width = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((TEXT_ENTRY_WIDTH_Y, TEXT_ENTRY_WIDTH_Y),
                                      (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, object_id="#text_entry_width", initial_text=str(board_width))
        self.text_entry_height = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((TEXT_ENTRY_HEIGHT_X, TEXT_ENTRY_HEIGHT_Y),
                                      (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, object_id="#text_entry_height", initial_text=str(board_height))
        self.text_entry_amount_mines = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((TEXT_ENTRY_AMOUNT_MINES_X, TEXT_ENTRY_AMOUNT_MINES_Y),
                                      (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, object_id="#text_entry_amount_mines", initial_text=str(amount_mines))
        self.button_create_board = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (BUTTON_CREATE_X, BUTTON_CREATE_Y),
                (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, object_id="#button_create_board",
            text="Create")
        self.text_mine_counter = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((TEXT_MINE_COUNTER_X, TEXT_MINE_COUNTER_Y), (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, html_text=str(amount_mines))

    def draw(self, surface) -> None:
        self.fill("gray50")
        surface.blit(self, dest=self.pos)
        self.options_manager.draw_ui(surface)

    def get_board_data(self):
        return int(self.text_entry_width.get_text()), int(self.text_entry_height.get_text()), int(
            self.text_entry_amount_mines.get_text())

    def update_mine_counter(self, mine_counter):
        self.text_mine_counter.set_text(str(mine_counter))
