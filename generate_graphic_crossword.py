import json

import pandas as pd
import pygame

from utilities.arrowed_definitions import get_arrowed_definitions
from utilities.definition import Definition, save_definitions_to_json
from utilities.graphical import (
    MARGIN_TRIANGLE,
    WIDTH_TRIANGLE,
    MARGIN,
    WIDTH,
    HEIGHT,
    WHITE,
    BLUE,
    BLUE_LIGHT,
    BLACK,
)


def get_definition_from_position(
    i: int, j: int, definition_type: str, definitions: list[Definition]
) -> Definition:
    return next(
        d
        for d in definitions
        if d["i"] == i and d["j"] == j and d["definition_type"] == definition_type
    )


def draw_grid(screen, df_map):
    # Draw the grid
    for row in range(len(df_map)):
        for column in range(len(df_map[row])):
            if df_map[row][column].isnumeric():
                color = WHITE
            else:
                color = BLUE
            pygame.draw.rect(
                screen,
                color,
                [
                    (MARGIN + WIDTH) * column + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN,
                    WIDTH,
                    HEIGHT,
                ],
            )
            if df_map[row][column].isnumeric():
                pygame.draw.rect(
                    screen,
                    BLACK,
                    [
                        (MARGIN + WIDTH) * column + MARGIN,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                    MARGIN,
                )


def draw_save_button(screen):
    save_rect = pygame.draw.rect(
        screen,
        WHITE,
        [
            550,
            20,
            WIDTH,
            HEIGHT,
        ],
    )
    pygame.draw.rect(
        screen,
        WHITE,
        [
            548,
            18,
            WIDTH + 8,
            HEIGHT + 8,
        ],
        MARGIN * 2,
    )
    font = pygame.font.SysFont("Futura", 18)
    img = font.render("SAVE", True, BLACK)
    screen.blit(img, (558, 38))
    return save_rect


def draw_arrow(screen, df_map):
    # Draw the arrows
    for row in range(len(df_map)):
        for column in range(len(df_map[row])):
            if df_map[row][column].isnumeric():
                for c in df_map[row][column]:
                    defi = get_arrowed_definitions(c)
                    base_triangle_x = (MARGIN + WIDTH) * (
                        column + getattr(defi, "j_diff")
                    )
                    base_triangle_y = (MARGIN + HEIGHT) * (
                        row + getattr(defi, "i_diff")
                    )

                    pygame.draw.polygon(
                        screen,
                        BLUE_LIGHT,
                        (
                            (
                                base_triangle_x + MARGIN_TRIANGLE,
                                base_triangle_y + MARGIN_TRIANGLE,
                            ),
                            (
                                base_triangle_x
                                + MARGIN_TRIANGLE
                                + WIDTH_TRIANGLE * (not getattr(defi, "is_horizontal")),
                                base_triangle_y
                                + MARGIN_TRIANGLE
                                + WIDTH_TRIANGLE * getattr(defi, "is_horizontal"),
                            ),
                            (
                                base_triangle_x + MARGIN_TRIANGLE + WIDTH_TRIANGLE / 2,
                                base_triangle_y + MARGIN_TRIANGLE + WIDTH_TRIANGLE / 2,
                            ),
                        ),
                    )


def draw_text(screen, definitions):
    # Draw the arrows
    for d in definitions:
        d.draw(screen)


def generate_graphic_crossword(filled_map: str):

    # Initialize pygame
    pygame.init()

    f = open(f"resources/filled_maps/{filled_map}.json")
    filled_map_json = json.load(f)
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

    df_map = pd.read_csv(
        f"resources/maps/{filled_map_json["map_file"]}.csv", header=None, sep=","
    )
    df_map = df_map.values.tolist()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [650, 675]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    text_editing = False
    last_definition = None
    text_filler = ""
    # -------- Main Program Loop -----------
    while not done:

        # Set the screen background
        screen.fill(BLACK)

        draw_grid(screen, df_map)
        save_rect = draw_save_button(screen)
        draw_arrow(screen, df_map)
        draw_text(screen, all_definitions)
        if text_editing:
            pygame.draw.rect(
                screen,
                BLACK,
                [
                    0,
                    0,
                    WIDTH * 2,
                    HEIGHT * 2,
                ],
            )
            font = pygame.font.SysFont("Futura", 20)
            img = font.render(text_filler, True, WHITE)
            screen.blit(img, (0, 0))

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
            if event.type == pygame.TEXTINPUT and text_editing:
                text_filler += event.text
            if event.type == event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_filler = text_filler[:-1]
                if event.key == pygame.K_RETURN:
                    for d in all_definitions:
                        if getattr(d, "word") == getattr(last_definition, "word"):
                            d.definition = text_filler
                    text_editing = False
                    text_filler = ""

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
