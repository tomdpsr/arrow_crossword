import pygame

from graphical_utilities.constants import WHITE, BLUE, MARGIN, WIDTH, HEIGHT, BLACK, BLUE_LIGHT, MARGIN_TRIANGLE, \
    WIDTH_TRIANGLE
from utilities.arrowed_definitions import get_arrowed_definitions


class MainPanel:
    def __init__(self, screen, width, height):
        self.subsurface = screen.subsurface(0, 0, width, height)

    def draw_grid(self, df_map):
        # Draw the grid
        for row in range(len(df_map)):
            for column in range(len(df_map[row])):
                if df_map[row][column].isnumeric():
                    color = WHITE
                else:
                    color = BLUE
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

    def draw_arrow(self, df_map):
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
                            self.subsurface,
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

    def draw_text(self, definitions):
        # Draw the arrows
        for d in definitions:
            d.draw_text(self.subsurface)
            d.draw_seperator(self.subsurface)
