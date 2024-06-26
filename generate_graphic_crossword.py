import datetime
import json

import pandas as pd
import pygame

from graphical_utilities.main_panel import MainPanel
from graphical_utilities.menu_panel import MenuPanel
from graphical_utilities.constants import (
    MARGIN,
    WIDTH,
    HEIGHT,
    BLACK, MENU_HEIGHT, DEFINITION_FONT_SIZE, MENU_FONT_SIZE, MAIN_FONT_PATH,
)
from utilities.definition.definition import Definition
from utilities.definition.utilities import save_definitions_to_json


def init_definitions(filled_map_json) -> list[Definition]:
    all_definitions = []
    for d in filled_map_json["definitions"]:
        dd = Definition(
            definition_type=d["definition_type"],
            i=d["i"],
            j=d["j"],
            word=d["word"],
            definition=d["definition"],
        )
        all_definitions.append(dd)

    # Sorry for the n square
    for d in all_definitions:
        if d.linked_definition is None:
            for d2 in all_definitions:
                if d.i == d2.i and d.j == d2.j and d.word != d2.word:
                    d.linked_definition, d2.linked_definition = d2, d
    return all_definitions

def generate_graphic_crossword(filled_map: str):
    # Initialize pygame
    pygame.init()

    f = open(f"resources/filled_maps/{filled_map}.json")
    filled_map_json = json.load(f)
    all_definitions = init_definitions(filled_map_json)

    df_map = pd.read_csv(
        f"resources/maps/{filled_map_json["map_file"]}.csv", header=None, sep=","
    )
    df_map = df_map.values.tolist()

    WINDOW_WIDTH = len(df_map[0]) * (WIDTH + MARGIN) + MARGIN
    WINDOW_HEIGHT = len(df_map) * (HEIGHT + MARGIN) + MARGIN

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT + MENU_HEIGHT]
    screen = pygame.display.set_mode(WINDOW_SIZE)


    # Surface
    game_sub_surface = MainPanel(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
    menu_sub_surface = MenuPanel(screen, WINDOW_HEIGHT, WINDOW_WIDTH)


    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    text_editing = False
    last_definition = None
    text_filler = ""
    screen.fill(BLACK)


    # Fonts
    menu_font = pygame.font.Font(MAIN_FONT_PATH, MENU_FONT_SIZE)
    definition_font = pygame.font.Font(MAIN_FONT_PATH, DEFINITION_FONT_SIZE)

    # -------- Main Program Loop -----------
    while not done:

        # Set the screen background
        screen.fill(BLACK)

        game_sub_surface.draw_grid(df_map)
        save_rect = menu_sub_surface.draw_save_button(menu_font)
        screen_rect = menu_sub_surface.draw_screen_button(menu_font)
        game_sub_surface.draw_arrow(df_map)
        (game_sub_surface.draw_definitions(all_definitions, definition_font))
        if text_editing:
            menu_sub_surface.draw_text_editing(last_definition, text_filler, menu_font)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not text_editing:
                    for definition in all_definitions:
                        if definition.is_clicked(event.pos):
                            text_editing = True
                            last_definition = definition
                            print(definition.definition)
                if save_rect.collidepoint(event.pos):
                    print("bouton")
                    save_definitions_to_json(
                        all_definitions,
                        filled_map_json["score"],
                        filled_map_json["map_file"],
                        filled_map,
                    )
                if screen_rect.collidepoint(event.pos):
                    print("screen")
                    pygame.image.save(game_sub_surface.subsurface, f"screen/export{filled_map}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.png")
            if event.type == pygame.TEXTINPUT and text_editing:
                text_filler += event.text
            if event.type == event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_filler = text_filler[:-1]
                if event.key == pygame.K_RETURN:
                    for d in all_definitions:
                        if getattr(d, "word") == getattr(last_definition, "word"):
                            d.update_definition(text_filler)
                    text_editing = False
                    text_filler = ""
                if event.key == pygame.K_ESCAPE:
                    text_editing = False
                    text_filler = ""

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
