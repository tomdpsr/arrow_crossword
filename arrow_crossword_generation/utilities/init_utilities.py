import json
import os

from shared_utilities.capelito.utilities import init_capelitos


def get_validated_custom_words() -> list:
    validated_custom_words = []
    for file in os.listdir('data/validated_capelitos'):
        if file.endswith('.json'):
            f = open(f'data/validated_capelitos/{file}')
            filled_map_json = json.load(f)
            all_capelitos = init_capelitos(filled_map_json)
            all_custom_words = [w.word for w in all_capelitos if w.is_custom_capelito]
            validated_custom_words = list(set(validated_custom_words + all_custom_words + [filled_map_json['mystery_capelito']['word']]))

    return validated_custom_words
