import json
import os

import pandas as pd

from arrow_crossword_generation.utilities.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
)
from arrow_crossword_generation.utilities.generation_utilities import (
    update_possible_values,
    update_definitions_from_game_state, shuffle_definitions,
)
from arrow_crossword_graphical_interface.generate_graphic_crossword import (
    init_definitions,
)
from shared_utilities.definition.definition import Definition


def init_state(
    df_init: pd.DataFrame, all_dictionaries: dict, validated_custom_words: list
):
    df_game_state = df_init.values.tolist()
    definitions = []
    for i in range(len(df_game_state)):
        for j in range(len(df_game_state[i])):
            if df_game_state[i][j].isnumeric():
                for digit in df_game_state[i][j]:
                    d = Definition(definition_type=digit, i=i, j=j)
                    definitions.append(d)
    definitions = update_definitions_from_game_state(definitions, df_game_state)
    definitions = shuffle_definitions(definitions)
    definitions, _ = update_possible_values(
        definitions, all_dictionaries, validated_custom_words
    )
    for i in range(len(definitions)):
        definitions[i].previous_word = definitions[i].word
    return df_game_state, definitions


def init_all_dictionaries(dict_folder: str):
    def init_dictionary(sub_dict_folder: str):
        sub_dict = {}
        for i in range(2, 25):
            dic_file = f"{DICTIONARY_TO_PATH[sub_dict_folder]}/{sub_dict_folder}/word_{i}.csv"
            if os.path.isfile(dic_file):
                df_words_file = open(
                    f"{DICTIONARY_TO_PATH[sub_dict_folder]}/{sub_dict_folder}/word_{i}.csv",
                    "r",
                    encoding="utf-8",
                )
                df_words = set([x.strip() for x in df_words_file])
            else:
                df_words = set()
            sub_dict[i] = df_words
        return sub_dict

    all_dictionaries = {
        DICTIONARY.CUSTOM_DICTIONARY: init_dictionary(DICTIONARY.CUSTOM_DICTIONARY),
        DICTIONARY.DEFAULT_DICTIONARY: init_dictionary(dict_folder),
        DICTIONARY.FORBIDDEN_DICTIONARY: init_dictionary(DICTIONARY.FORBIDDEN_DICTIONARY),
    }
    return all_dictionaries


def get_validated_custom_words() -> list:
    validated_custom_words = []
    for file in os.listdir("data/validated_definitions"):
        f = open(f"data/validated_definitions/{file}")
        filled_map_json = json.load(f)
        all_definitions = init_definitions(filled_map_json)
        all_custom_words = [w.word for w in all_definitions if w.is_custom_definition]
        validated_custom_words = list(set(validated_custom_words + all_custom_words + [filled_map_json['mystery_word']['word']]))

    return validated_custom_words
