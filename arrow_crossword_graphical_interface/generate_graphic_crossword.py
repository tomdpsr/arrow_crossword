import datetime
import json

import pygame

from arrow_crossword_graphical_interface.utilities.constants import (
    WIDTH,
    MARGIN,
    HEIGHT,
    MENU_HEIGHT,
    MAIN_FONT_PATH,
    BLACK,
    LETTER_FONT_SIZE,
    MENU_FONT_SIZE,
    DEFINITION_FONT_SIZE,
    WHITE,
    PANEL_MYSTERY_WORD_HEIGHT,
    TEXT_EDITING, ITALIC_FONT_PATH, MYSTERY_FONT_SIZE, BLUE_LIGHT, BLUE, GREY, GREY_LIGHT,
)
from arrow_crossword_graphical_interface.utilities.main_panel import MainPanel
from arrow_crossword_graphical_interface.utilities.menu_panel import MenuPanel
from shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword


def generate_graphic_crossword(arrow_crossword: ArrowCrossword):
    # Initialize pygame
    pygame.init()

    WINDOW_WIDTH = len(arrow_crossword.game_state[0]) * (WIDTH + MARGIN) + MARGIN
    WINDOW_HEIGHT = len(arrow_crossword.game_state) * (HEIGHT + MARGIN) + MARGIN

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [
        WINDOW_WIDTH,
        WINDOW_HEIGHT + MENU_HEIGHT + PANEL_MYSTERY_WORD_HEIGHT,
    ]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Surface
    game_sub_surface = MainPanel(
        screen=screen,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT + PANEL_MYSTERY_WORD_HEIGHT,
        mystery_capelito=arrow_crossword.mystery_capelito
    )
    menu_sub_surface = MenuPanel(
        screen=screen, start_height=WINDOW_HEIGHT + PANEL_MYSTERY_WORD_HEIGHT, width=WINDOW_WIDTH
    )

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    text_editing = None
    with_letters = False
    last_capelito = None
    text_filler = ""
    screen.fill(BLACK)

    # Fonts
    menu_font = pygame.font.Font(MAIN_FONT_PATH, MENU_FONT_SIZE)
    capelito_font = pygame.font.Font(MAIN_FONT_PATH, DEFINITION_FONT_SIZE)
    capelito_font_italic = pygame.font.Font(ITALIC_FONT_PATH, DEFINITION_FONT_SIZE)
    mystery_font = pygame.font.Font(MAIN_FONT_PATH, MYSTERY_FONT_SIZE)
    letter_font = pygame.font.Font(MAIN_FONT_PATH, LETTER_FONT_SIZE)

    # -------- Main Program Loop -----------
    while not done:

        # Set the screen background
        screen.fill(WHITE)
        game_sub_surface.subsurface.fill(BLACK)
        menu_sub_surface.subsurface.fill(BLACK)

        # different color
        if with_letters:
            color_arrow = GREY_LIGHT
            color_back = GREY
        else:
            color_arrow = BLUE_LIGHT
            color_back = BLUE

        game_sub_surface.draw_grid(arrow_crossword.game_state, color_back)
        save_rect = menu_sub_surface.draw_save_button(menu_font)
        screen_rect = menu_sub_surface.draw_screen_button(menu_font)
        letter_rect = menu_sub_surface.draw_letter_button(menu_font)
        game_sub_surface.draw_arrow(arrow_crossword.game_state, color_arrow)
        game_sub_surface.draw_capelitos(
            arrow_crossword.capelitos, capelito_font, capelito_font_italic, letter_font, with_letters
        )
        game_sub_surface.draw_mystery_capelito_boxes(capelito_font)
        mystery_capelito_rect = game_sub_surface.draw_mystery_capelito(
            mystery_font
        )
        game_sub_surface.draw_grid_numbers(capelito_font)
        if text_editing:
            menu_sub_surface.draw_text_editing(last_capelito, text_filler, menu_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not text_editing:
                    for capelito in arrow_crossword.capelitos:
                        if capelito.is_clicked(event.pos):
                            text_editing = TEXT_EDITING.WORD_DEFINITION
                            last_capelito = capelito
                    if mystery_capelito_rect.collidepoint(event.pos):
                        text_editing = TEXT_EDITING.MYSTERY_DEFINITION
                if save_rect.collidepoint(event.pos):
                    arrow_crossword.save_arrow_crossword_to_json()
                if screen_rect.collidepoint(event.pos):
                    if with_letters:
                        surface_to_screen = game_sub_surface.subsurface
                        suffix = '_wl'
                    else:
                        surface_to_screen = game_sub_surface.main_surface
                        suffix = ''

                    pygame.image.save(
                        surface_to_screen,
                        f"data/screen/export{arrow_crossword.filename}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}{suffix}.png",
                    )
                if letter_rect.collidepoint(event.pos):
                    with_letters = not with_letters
            if event.type == pygame.TEXTINPUT and text_editing:
                text_filler += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_filler = text_filler[:-1]
                if event.key == pygame.K_RETURN:
                    if text_editing == TEXT_EDITING.WORD_DEFINITION:
                        for c in arrow_crossword.capelitos:
                            if getattr(c, "word") == getattr(last_capelito, "word"):
                                c.update_definition(text_filler)
                    if text_editing == TEXT_EDITING.MYSTERY_DEFINITION:
                        game_sub_surface.mystery_capelito["capelito"] = text_filler
                    text_editing = None
                    text_filler = ""
                if event.key == pygame.K_ESCAPE:
                    text_editing = None
                    text_filler = ""

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
