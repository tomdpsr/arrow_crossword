import textwrap
from dataclasses import dataclass

import pygame

from arrow_crossword_graphical_interface.utilities.constants import (
    BLACK,
    MARGIN,
    WIDTH,
    HEIGHT,
    DEFINITION_FONT_SIZE,
    PANEL_MYSTERY_WORD_HEIGHT,
)
from shared_utilities.arrowed_place_holder.arrowed_place_holder import (
    get_arrowed_place_holder,
    ArrowedPlaceHolder,
)


@dataclass
class Capelito:
    capelito_type: str
    i: int
    j: int
    is_custom_capelito: bool = False
    arrowed_place_holder: ArrowedPlaceHolder = None
    word: str = ""
    previous_word: str = ""
    is_set: bool = False
    possible_values = []
    nb_tries: int = 0
    definition: str = ""
    wrapped_capelito = None
    linked_capelito = None
    rects = []

    def __eq__(self, other):
        return (
            self.i == other.i
            and self.j == other.j
            and self.capelito_type == other.capelito_type
        )

    def __hash__(self):
        return hash((self.i, self.j, self.capelito_type))

    def __post_init__(self):
        self.update_definition(self.definition)
        self.arrowed_place_holder = get_arrowed_place_holder(self.capelito_type)

    def update_definition(self, new_definition):
        self.definition = new_definition
        wrapped_capelito = textwrap.wrap(self.definition, width=11, max_lines=3)
        for index, w in enumerate(wrapped_capelito[1:]):
            if f" {w}" not in self.definition:
                wrapped_capelito[index + 1] = "-" + wrapped_capelito[index + 1]
        self.wrapped_capelito = wrapped_capelito

    @staticmethod
    def calculate_diff(iterate: int, nb_values: int, center_case):
        diff_j = 0
        if nb_values == 1:
            diff_j = center_case
        if nb_values == 2:
            if iterate == 0:
                diff_j = center_case - (DEFINITION_FONT_SIZE / 2)
            if iterate == 1:
                diff_j = center_case + (DEFINITION_FONT_SIZE / 2)
        if nb_values == 3:
            if iterate == 0:
                diff_j = center_case - DEFINITION_FONT_SIZE
            if iterate == 1:
                diff_j = center_case
            if iterate == 2:
                diff_j = center_case + DEFINITION_FONT_SIZE
        return diff_j

    @staticmethod
    def calculate_center(self_nb_values: int, linked_nb_values: int):
        return self_nb_values * HEIGHT / (self_nb_values + linked_nb_values)

    def calculate_center_subdivision(self, self_nb_values: int, linked_nb_values: int):
        center = self.calculate_center(self_nb_values, linked_nb_values)
        is_upper_location = self.arrowed_place_holder.upper_location
        if is_upper_location:
            return center / 2
        else:
            return HEIGHT - (center / 2)

    def draw_capelito(self, screen, font, font_italic):
        images, self.rects = [], []
        for wd in range(len(self.wrapped_capelito)):
            if self.is_custom_capelito:
                image = font_italic.render(self.wrapped_capelito[wd].upper(), True, BLACK)
            else:
                image = font.render(self.wrapped_capelito[wd].upper(), True, BLACK)
            images.append(image)
            if self.linked_capelito is not None:
                center_case = self.calculate_center_subdivision(
                    len(self.wrapped_capelito),
                    len(self.linked_capelito.wrapped_capelito),
                )
            else:
                center_case = HEIGHT / 2
            diff_j = self.calculate_diff(wd, len(self.wrapped_capelito), center_case)
            rect = image.get_rect(
                center=(
                    ((MARGIN + WIDTH) * self.j + MARGIN + WIDTH / 2),
                    (MARGIN + HEIGHT) * self.i + MARGIN + diff_j,
                )
            )
            self.rects.append(rect)
        for i in range(len(self.wrapped_capelito)):
            screen.blit(images[i], self.rects[i])

        # Redraw rect for mystery diff
        for r in range(len(self.rects)):
            self.rects[r] = self.rects[r].move(0, PANEL_MYSTERY_WORD_HEIGHT)

    def draw_capelito_letters(self, screen, font):
        letter_i = self.i + self.arrowed_place_holder.i_diff
        letter_j = self.j + self.arrowed_place_holder.j_diff
        for l in self.word:
            letter = font.render(l.upper(), True, BLACK)
            rect = letter.get_rect(
                center=(
                    ((MARGIN + WIDTH) * letter_j + MARGIN + WIDTH / 2),
                    (MARGIN + HEIGHT) * letter_i + MARGIN + HEIGHT / 2,
                ),
            )
            screen.blit(letter, rect)
            if self.arrowed_place_holder.is_horizontal:
                letter_j += 1
            else:
                letter_i += 1

    def draw_seperator(self, screen):
        if (
            self.linked_capelito is not None
            and self.arrowed_place_holder.upper_location
        ):
            center_case = self.calculate_center(
                len(self.wrapped_capelito),
                len(self.linked_capelito.wrapped_capelito),
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
            "capelito_type": self.capelito_type,
            "i": self.i,
            "j": self.j,
            "word": self.word,
            "definition": self.definition,
            "is_custom_capelito": self.is_custom_capelito,
        }
