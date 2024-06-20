import datetime
import json
from dataclasses import dataclass

import pygame

from utilities.arrowed_definitions import get_arrowed_definitions
from utilities.graphical import BLACK, MARGIN, WIDTH, HEIGHT


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
    linked_definition = None

    def __post_init__(self):
        self.update_image()

    def update_image(self):
        font = pygame.font.SysFont("Futura", 7, bold=True)
        self.image = font.render(self.definition.upper(), True, BLACK)
        self.rect = self.image.get_rect(
            center=(
                ((MARGIN + WIDTH) * self.j + MARGIN + WIDTH / 2),
                (MARGIN + HEIGHT) * self.i + MARGIN + HEIGHT / 2,
            )
        )

    def draw(self, screen):
        self.update_image()
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

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
