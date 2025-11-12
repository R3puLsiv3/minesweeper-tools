from pygame import Surface
import pygame_gui
import pygame


class OptionsView(Surface):

    def __init__(self, width, height, manager):
        super().__init__((width, height))
        self.manager = manager
        self.width_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 30), (50, 30)),

                                                               manager=self.manager, object_id="width_input")

        self.height_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((90, 30), (50, 30)),
                                                                manager=self.manager, object_id="height_input")
        self.create_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 30), (50, 30)),
                                                          manager=self.manager, object_id="create_button",
                                                          text="Go")

    def draw_options(self):
        self.manager.update(0.001)
        self.manager.draw_ui(self)
