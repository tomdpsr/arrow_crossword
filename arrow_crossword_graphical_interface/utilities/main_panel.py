import pygame

from arrow_crossword_graphical_interface.utilities.constants import (
    WHITE,
    MARGIN,
    WIDTH,
    HEIGHT,
    BLACK,
    MARGIN_TRIANGLE,
    WIDTH_TRIANGLE,
    PANEL_MYSTERY_WORD_HEIGHT,
    MYSTERY_BOX_WIDTH,
    MYSTERY_BOX_HEIGHT,
)
from shared_utilities.arrowed_place_holder.arrowed_place_holder import (
    get_arrowed_place_holder,
)


class MainPanel:
    def __init__(self, screen, width, height, mystery_capelito):
        self.main_surface = screen.subsurface(0, 0, width, height)
        self.subsurface = self.main_surface.subsurface(
            0, PANEL_MYSTERY_WORD_HEIGHT, width, height - PANEL_MYSTERY_WORD_HEIGHT
        )
        self.width = width
        self.mystery_subsurface = self.main_surface.subsurface(
            0, 0, width, PANEL_MYSTERY_WORD_HEIGHT
        )
        if mystery_capelito:
            self.mystery_capelito = mystery_capelito

    def draw_grid(self, df_map, base_color):
        # Draw the grid
        for row in range(len(df_map)):
            for column in range(len(df_map[row])):
                if df_map[row][column].isnumeric():
                    color = WHITE
                else:
                    color = base_color
                pygame.draw.rect(
                    self.subsurface,
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
                        self.subsurface,
                        BLACK,
                        [
                            (MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH,
                            HEIGHT,
                        ],
                        MARGIN,
                    )

    def draw_grid_numbers(self, font):
        # Draw the grid
        for letter in range(len(self.mystery_capelito["word_letters"])):
            (_, i, j) = self.mystery_capelito["word_letters"][letter]
            letter_number = font.render(f"{letter + 1}", True, BLACK)
            rect = letter_number.get_rect(
                topright=(
                    (MARGIN + WIDTH) * (j + 1) - MARGIN,
                    ((MARGIN + HEIGHT) * i) + MARGIN,
                ),
            )
            self.subsurface.blit(letter_number, rect)

    def draw_arrow(self, df_map, color):
        # Draw the arrows
        for row in range(len(df_map)):
            for column in range(len(df_map[row])):
                if df_map[row][column].isnumeric():
                    for c in df_map[row][column]:
                        defi = get_arrowed_place_holder(c)
                        base_triangle_x = (MARGIN + WIDTH) * (
                            column + getattr(defi, "j_diff")
                        )
                        base_triangle_y = (MARGIN + HEIGHT) * (
                            row + getattr(defi, "i_diff")
                        )

                        pygame.draw.polygon(
                            self.subsurface,
                            color,
                            (
                                (
                                    base_triangle_x + MARGIN_TRIANGLE,
                                    base_triangle_y + MARGIN_TRIANGLE,
                                ),
                                (
                                    base_triangle_x
                                    + MARGIN_TRIANGLE
                                    + WIDTH_TRIANGLE
                                    * (not getattr(defi, "is_horizontal")),
                                    base_triangle_y
                                    + MARGIN_TRIANGLE
                                    + WIDTH_TRIANGLE * getattr(defi, "is_horizontal"),
                                ),
                                (
                                    base_triangle_x
                                    + MARGIN_TRIANGLE
                                    + WIDTH_TRIANGLE / 2,
                                    base_triangle_y
                                    + MARGIN_TRIANGLE
                                    + WIDTH_TRIANGLE / 2,
                                ),
                            ),
                        )

    def draw_capelitos(
        self, capelitos, capelito_font, capelito_font_italic, letter_font, with_capelito_letters: bool
    ):
        # Draw the arrows
        for d in capelitos:
            d.draw_capelito(self.subsurface, capelito_font, capelito_font_italic)
            d.draw_seperator(self.subsurface)
            if with_capelito_letters:
                d.draw_capelito_letters(self.subsurface, letter_font)

    def draw_mystery_capelito_boxes(self, font):
        # Draw the arrows
        for i in range(len(self.mystery_capelito["word_letters"])):
            pygame.draw.rect(
                self.mystery_subsurface,
                BLACK,
                [
                    self.width - ((MARGIN * 2 + MYSTERY_BOX_WIDTH) * (i + 1) + MARGIN),
                    PANEL_MYSTERY_WORD_HEIGHT - (MARGIN * 10 + MYSTERY_BOX_WIDTH),
                    MYSTERY_BOX_WIDTH,
                    MYSTERY_BOX_HEIGHT,
                ],
                MARGIN,
            )
            letter_number = font.render(
                f"{len(self.mystery_capelito['word_letters'])-i}", True, BLACK
            )
            rect = letter_number.get_rect(
                topright=(
                    self.width - ((MARGIN * 2 + MYSTERY_BOX_WIDTH) * i + MARGIN * 5),
                    PANEL_MYSTERY_WORD_HEIGHT - (MARGIN * 10 + MYSTERY_BOX_WIDTH),
                ),
            )
            self.mystery_subsurface.blit(letter_number, rect)

    def draw_mystery_capelito(self, font):
        # Draw the arrows
        letter_number = font.render(self.mystery_capelito["definition"].upper(), True, BLACK)
        mystery_capelito_rect = letter_number.get_rect(
            bottomright=(
                self.width - MARGIN*2,
                PANEL_MYSTERY_WORD_HEIGHT - (MARGIN * 15 + MYSTERY_BOX_WIDTH),
            ),
        )
        self.mystery_subsurface.blit(letter_number, mystery_capelito_rect)
        return mystery_capelito_rect
