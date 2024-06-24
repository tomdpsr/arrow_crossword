import pygame
from pygame import Rect

from graphical_utilities.constants import WHITE, BLUE, MARGIN, WIDTH, HEIGHT, BLACK, BLUE_LIGHT, MARGIN_TRIANGLE, \
    WIDTH_TRIANGLE, MENU_HEIGHT, MAIN_FONT
from utilities.arrowed_definitions import get_arrowed_definitions


class MenuPanel:
    def __init__(self, screen, start_height, width):
        self.width = width
        self.start_height = start_height
        self.subsurface = screen.subsurface(0, start_height, self.width, MENU_HEIGHT)


    def draw_button(self, text, x, y):
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
                x-2,
                y-2,
                WIDTH + 8,
                HEIGHT + 8,
            ],
            MARGIN * 2,
        )
        font_size = int(20-(len(text)/2))
        font = pygame.font.SysFont(MAIN_FONT, font_size)
        img = font.render(text, True, BLACK)
        self.subsurface.blit(img, img.get_rect(center=button_rect.center))
        return button_rect.move(0, self.start_height)

    def draw_save_button(self):
        return self.draw_button('SAVE', 20, 20)


    def draw_screen_button(self):
        return self.draw_button('SCREEN', self.width-100, 20)

    def draw_text_editing(self, last_definition, text_filler):
        font = pygame.font.SysFont(MAIN_FONT, 13)
        self.subsurface.blit(font.render("Nouvelle définition", True, WHITE), (110, 20))
        self.subsurface.blit(
            font.render(f"Mot : [{last_definition.word}]", True, WHITE), (110, 35)
        )
        self.subsurface.blit(font.render("->", True, WHITE), (110, 50))
        self.subsurface.blit(font.render(text_filler, True, WHITE), (125, 50))

    def draw_screenshot_button(self):
        save_rect = pygame.draw.rect(
            self.subsurface,
            WHITE,
            [
                20,
                20,
                WIDTH,
                HEIGHT,
            ],
        )
        pygame.draw.rect(
            self.subsurface,
            WHITE,
            [
                18,
                18,
                WIDTH + 8,
                HEIGHT + 8,
            ],
            MARGIN * 2,
        )
        font = pygame.font.SysFont(MAIN_FONT, 18)
        img = font.render("SAVE", True, BLACK)
        self.subsurface.blit(img, (30, 40))
        return save_rect
