import datetime
import json
import textwrap
from dataclasses import dataclass

import pygame

from utilities.arrowed_definitions import get_arrowed_definitions
from graphical_utilities.constants import BLACK, MARGIN, WIDTH, HEIGHT, MAIN_FONT

FONT_SIZE = 8


@dataclass
class Definition:
    definition_type: str
    i: int
    j: int
    word: str = ""
    previous_word: str = ""
    is_set: bool = False
    possible_values = []
    nb_tries: int = 0
    definition: str = ""
    wrapped_definition = None
    linked_definition = None
    rects = []
    images = []

    def __post_init__(self):
        self.update_definition(self.definition)
        self.update_images()

    def update_definition(self, new_definition):
        self.definition = new_definition
        wrapped_definition = textwrap.wrap(self.definition, width=11, max_lines=3)
        for index, w in enumerate(wrapped_definition[1:]):
            if f" {w}" not in self.definition:
                wrapped_definition[index + 1] = "-" + wrapped_definition[index + 1]
        self.wrapped_definition = wrapped_definition

    @staticmethod
    def calculate_diff(iterate: int, nb_values: int, center_case):
        diff_j = 0
        if nb_values == 1:
            diff_j = center_case
        if nb_values == 2:
            if iterate == 0:
                diff_j = center_case - (FONT_SIZE / 2)
            if iterate == 1:
                diff_j = center_case + (FONT_SIZE / 2)
        if nb_values == 3:
            if iterate == 0:
                diff_j = center_case - FONT_SIZE
            if iterate == 1:
                diff_j = center_case
            if iterate == 2:
                diff_j = center_case + FONT_SIZE
        return diff_j

    def calculate_center(self, self_nb_values: int, linked_nb_values: int):
        return self_nb_values * HEIGHT / (self_nb_values + linked_nb_values)

    def calculate_center_subdivision(self, self_nb_values: int, linked_nb_values: int):
        center = self.calculate_center(self_nb_values, linked_nb_values)
        is_upper_location = getattr(
            get_arrowed_definitions(self.definition_type), "upper_location"
        )
        if is_upper_location:
            return center / 2
        else:
            return HEIGHT - (center / 2)

    def update_images(self):
        font = pygame.font.SysFont(MAIN_FONT, FONT_SIZE, bold=True)
        self.images, self.rects = [], []
        for wd in range(len(self.wrapped_definition)):
            image = font.render(self.wrapped_definition[wd].upper(), True, BLACK)
            self.images.append(image)
            if self.linked_definition is not None:
                center_case = self.calculate_center_subdivision(
                    len(self.wrapped_definition),
                    len(self.linked_definition.wrapped_definition),
                )
            else:
                center_case = HEIGHT / 2
            diff_j = self.calculate_diff(wd, len(self.wrapped_definition), center_case)
            rect = image.get_rect(
                center=(
                    ((MARGIN + WIDTH) * self.j + MARGIN + WIDTH / 2),
                    (MARGIN + HEIGHT) * self.i + MARGIN + diff_j,
                )
            )
            self.rects.append(rect)

    def draw_text(self, screen):
        self.update_images()
        for i in range(len(self.wrapped_definition)):
            screen.blit(self.images[i], self.rects[i])

    def draw_seperator(self, screen):
        is_upper_location = getattr(
            get_arrowed_definitions(self.definition_type), "upper_location"
        )
        if self.linked_definition is not None and is_upper_location:
            center_case = self.calculate_center(
                len(self.wrapped_definition),
                len(self.linked_definition.wrapped_definition),
            )

            pygame.draw.line(
                screen,
                BLACK,
                (
                    (MARGIN + WIDTH) * self.j + MARGIN,
                    (MARGIN + WIDTH) * self.i + MARGIN + center_case,
                ),
                (
                    (MARGIN + WIDTH) * self.j + MARGIN + WIDTH,
                    (MARGIN + WIDTH) * self.i + MARGIN + center_case,
                ),
                MARGIN,
            )

    def is_clicked(self, pos):
        for r in self.rects:
            if r.collidepoint(pos):
                return True
        return False

    def export_to_dict(self) -> dict:
        return {
            "definition_type": self.definition_type,
            "i": self.i,
            "j": self.j,
            "word": self.word,
            "definition": self.definition,
        }


def save_definitions_to_json(
    definitions: list[Definition], score: int, map_file: str, filled_map_file=None
) -> None:
    filled_map_file = (
        filled_map_file or f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{score}"
    )
    data_to_export = {
        "map_file": map_file,
        "score": score,
        "date": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "definitions": [d.export_to_dict() for d in definitions],
    }
    with open(
        f"resources/filled_maps/{filled_map_file}.json",
        "w",
    ) as f:
        json.dump(data_to_export, f)
