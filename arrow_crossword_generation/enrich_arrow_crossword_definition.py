import json

from arrow_crossword_generation.utilities.post_generation_utilities import get_open_ai_dictionaries, \
    enrich_non_custom_definitions
from arrow_crossword_graphical_interface.generate_graphic_crossword import init_definitions
from shared_utilities.definition.utilities import save_definitions_to_json


def enrich_arrow_crossword_definition(definitions: str):
    f = open(f"data/definitions/{definitions}.json")
    filled_map_json = json.load(f)
    all_definitions = init_definitions(filled_map_json)

    all_definitions = enrich_non_custom_definitions(all_definitions)

    save_definitions_to_json(
        definitions=all_definitions,
        score=filled_map_json["score"],
        map_file=filled_map_json["map_file"],
        definition_file=definitions,
        mystery_word=filled_map_json["mystery_word"],
    )




