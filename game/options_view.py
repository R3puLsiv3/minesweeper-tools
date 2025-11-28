from pygame import Surface
import pygame_gui
import pygame
from config import OPTION_WIDTH, OPTION_HEIGHT, OPTIONS_X, OPTIONS_Y, TEXT_ENTRY_WIDTH_X, TEXT_ENTRY_WIDTH_Y, \
    TEXT_ENTRY_HEIGHT_X, \
    TEXT_ENTRY_HEIGHT_Y, BUTTON_CREATE_X, BUTTON_CREATE_Y


class OptionsView(Surface):

    def __init__(self, width: int, height: int, manager) -> None:
        super().__init__(size=(width, height))
        self.pos = (OPTIONS_X, OPTIONS_Y)
        self.options_manager = manager
        self.text_entry_width = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((TEXT_ENTRY_WIDTH_Y, TEXT_ENTRY_WIDTH_Y),
                                      (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, object_id="#text_entry_width")
        self.text_entry_height = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((TEXT_ENTRY_HEIGHT_X, TEXT_ENTRY_HEIGHT_Y),
                                      (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, object_id="#text_entry_height")
        self.button_create_board = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (BUTTON_CREATE_X, BUTTON_CREATE_Y),
                (OPTION_WIDTH, OPTION_HEIGHT)),
            manager=self.options_manager, object_id="#button_create_board",
            text="Create")

    def draw(self, surface) -> None:
        self.fill("gray50")
        surface.blit(self, dest=self.pos)
        self.options_manager.draw_ui(surface)
