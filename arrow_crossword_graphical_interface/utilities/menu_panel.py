import pygame

from arrow_crossword_graphical_interface.utilities.constants import (
    WHITE,
    MARGIN,
    WIDTH,
    HEIGHT,
    BLACK,
    MENU_HEIGHT,
)


class MenuPanel:
    def __init__(self, screen, start_height, width):
        self.width = width
        self.start_height = start_height
        self.subsurface = screen.subsurface(0, start_height, self.width, MENU_HEIGHT)

    def draw_button(self, text, x, y, font):
        button_rect = pygame.draw.rect(
            self.subsurface,
            WHITE,
            [
                x,
                y,
                WIDTH,
                HEIGHT,
            ],
        )
        pygame.draw.rect(
            self.subsurface,
            WHITE,
            [
                x - 2,
                y - 2,
                WIDTH + 8,
                HEIGHT + 8,
            ],
            MARGIN * 2,
        )
        img = font.render(text, True, BLACK)
        self.subsurface.blit(img, img.get_rect(center=button_rect.center))
        return button_rect.move(0, self.start_height)

    def draw_save_button(self, font):
        return self.draw_button("SAVE", 20, 20, font)

    def draw_screen_button(self, font):
        return self.draw_button("SCREEN", self.width - 100, 20, font)

    def draw_letter_button(self, font):
        return self.draw_button("LETTERS", self.width - 200, 20, font)

    def draw_text_editing(self, last_capelito, text_filler, font):
        self.subsurface.blit(font.render("Nouvelle définition", True, WHITE), (110, 20))
        if last_capelito:
            self.subsurface.blit(
                font.render(f"Mot : [{last_capelito.word}]", True, WHITE), (110, 35)
            )
        self.subsurface.blit(font.render("->", True, WHITE), (110, 50))
        self.subsurface.blit(font.render(text_filler, True, WHITE), (125, 50))
