import click
import fire

from arrow_crossword_generation.enrich_arrow_crossword_definition import (
    enrich_arrow_crossword_definition,
)
from arrow_crossword_generation.enrich_mystery_capelito import enrich_mystery_capelito
from arrow_crossword_generation.generate_arrow_crossword import generate_arrow_crossword
from arrow_crossword_graphical_interface.generate_graphic_crossword import (
    generate_graphic_crossword,
)
from shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword
from shared_utilities.dictionary_handler.constants import DICTIONARY


class GenerateArrowCrossword(object):
    arrow_crossword = None

    def __init__(self, arrow_crossword_file_path=None):
        self.arrow_crossword = ArrowCrossword(file_path=arrow_crossword_file_path)

    def generate_arrow_crosswords(self, dictionary, map_file):
        self.arrow_crossword = generate_arrow_crossword(dictionary, map_file)
        self.arrow_crossword.save_arrow_crossword_to_json()

    def enrich_mystery_capelitos(self):
        self.arrow_crossword = enrich_mystery_capelito(self.arrow_crossword)
        self.arrow_crossword.save_arrow_crossword_to_json()

    def enrich_arrow_crossword_definitions(self):
        self.arrow_crossword = enrich_arrow_crossword_definition(self.arrow_crossword)
        self.arrow_crossword.save_arrow_crossword_to_json()

    def generate_graphic_crossword(self):
        generate_graphic_crossword(self.arrow_crossword)

    def generate_and_enrich(
        self, dictionary=DICTIONARY.FRENCH_DICTIONARY, map_file="map_s"
    ):
        self.generate_arrow_crosswords(dictionary, map_file)
        self.enrich_mystery_capelitos()
        self.enrich_arrow_crossword_definitions()
        self.generate_graphic_crossword()


if __name__ == "__main__":
    fire.Fire(GenerateArrowCrossword)
