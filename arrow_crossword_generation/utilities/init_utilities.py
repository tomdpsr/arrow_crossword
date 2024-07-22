import json
import os

import pandas as pd

from arrow_crossword_generation.utilities.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
)
from arrow_crossword_generation.utilities.generation_utilities import (
    update_possible_values,
    update_capelitos_from_game_state, shuffle_capelitos,
)
from arrow_crossword_graphical_interface.generate_graphic_crossword import (
    init_capelitos,
)
from shared_utilities.capelito.capelito import Capelito


def init_state(
    df_init: pd.DataFrame, all_dictionaries: dict, validated_custom_words: list
):
    df_game_state = df_init.values.tolist()
    capelitos = []
    for i in range(len(df_game_state)):
        for j in range(len(df_game_state[i])):
            if df_game_state[i][j].isnumeric():
                for digit in df_game_state[i][j]:
                    capelitos.append(Capelito(capelito_type=digit, i=i, j=j))
    capelitos = update_capelitos_from_game_state(capelitos, df_game_state)
    capelitos = shuffle_capelitos(capelitos)
    capelitos, _ = update_possible_values(
        capelitos, all_dictionaries, validated_custom_words
    )
    for i in range(len(capelitos)):
        capelitos[i].previous_word = capelitos[i].word
    return df_game_state, capelitos


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
    for file in os.listdir('data/validated_capelitos'):
        if file.endswith('.json'):
            f = open(f'data/validated_capelitos/{file}')
            filled_map_json = json.load(f)
            all_capelitos = init_capelitos(filled_map_json)
            all_custom_words = [w.word for w in all_capelitos if w.is_custom_capelito]
            validated_custom_words = list(set(validated_custom_words + all_custom_words + [filled_map_json['mystery_capelito']['word']]))

    return validated_custom_words
