import json

from arrow_crossword_generation.utilities.post_generation_utilities import get_open_ai_dictionaries, \
    enrich_non_custom_capelitos
from arrow_crossword_graphical_interface.generate_graphic_crossword import init_capelitos
from shared_utilities.capelito.utilities import save_capelitos_to_json


def enrich_arrow_crossword_definition(capelitos: str):
    f = open(f"data/capelitos/{capelitos}.json")
    filled_map_json = json.load(f)
    all_capelitos = init_capelitos(filled_map_json)

    all_capelitos = enrich_non_custom_capelitos(all_capelitos)

    save_capelitos_to_json(
        capelitos=all_capelitos,
        score=filled_map_json["score"],
        map_file=filled_map_json["map_file"],
        capelito_file=capelitos,
        mystery_capelito=filled_map_json["mystery_capelito"],
    )




