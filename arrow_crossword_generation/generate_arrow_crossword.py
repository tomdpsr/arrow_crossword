import re
from random import shuffle
from typing import Tuple, List

import pandas as pd
import pygame

from arrow_crossword_generation.utilities.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
    THRESHOLD,
)
from shared_utilities.arrowed_place_holder.arrowed_place_holder import (
    get_arrowed_place_holder,
)
from shared_utilities.definition.definition import Definition
from shared_utilities.definition.utilities import save_definitions_to_json


def get_possibles_values_from_dic(letters, sub_dict: dict, set_words: list) -> list:
    r = re.compile(rf"{letters}")
    possible_values = list(filter(r.match, sub_dict[len(letters)]))
    # possible_values = list(set(possible_values) - set(set_words))
    shuffle(possible_values)
    return possible_values


def update_definitions_from_game_state(
    definitions: list[Definition],
    df_game_state: list[list[str]],
    all_dictionaries: dict,
) -> list[Definition]:
    for definition in definitions:
        arrowed_place_holder = get_arrowed_place_holder(definition.definition_type)
        letters = ""
        i = definition.i + arrowed_place_holder.i_diff
        j = definition.j + arrowed_place_holder.j_diff
        while not (df_game_state[i][j].isnumeric()):
            letters += df_game_state[i][j]
            if arrowed_place_holder.is_horizontal:
                j += 1
            else:
                i += 1
            if j == len(df_game_state[0]) or i == len(df_game_state):
                break
        definition.word = letters

        # get possible values
        if not definition.is_set:
            set_words = [d.word for d in definitions]
            custom_possible_values = get_possibles_values_from_dic(
                letters, all_dictionaries[DICTIONARY.CUSTOM_DICTIONARY], set_words
            )
            default_possible_values = get_possibles_values_from_dic(
                letters, all_dictionaries[DICTIONARY.DEFAULT_DICTIONARY], set_words
            )
            definition.possible_values = (
                default_possible_values + custom_possible_values
            )
            definition.nb_tries = 0

    return definitions


def set_letters(
    definition: Definition, df_game_state: list[list[str]]
) -> list[list[str]]:
    arrowed_place_holder = get_arrowed_place_holder(definition.definition_type)
    i = definition.i + arrowed_place_holder.i_diff
    j = definition.j + arrowed_place_holder.j_diff
    for l in definition.word:
        df_game_state[i][j] = l
        if arrowed_place_holder.is_horizontal:
            j += 1
        else:
            i += 1
    return df_game_state


def init_state(df_init: pd.DataFrame, all_dictionaries: dict):
    df_game_state = df_init.values.tolist()
    definitions = []
    for i in range(len(df_game_state)):
        for j in range(len(df_game_state[i])):
            if df_game_state[i][j].isnumeric():
                for digit in df_game_state[i][j]:
                    d = Definition(definition_type=digit, i=i, j=j)
                    definitions.append(d)
    definitions = update_definitions_from_game_state(
        definitions, df_game_state, all_dictionaries
    )
    definitions = sorted(definitions, key=lambda x: len(x.word), reverse=True)
    for i in range(len(definitions)):
        definitions[i].previous_word = definitions[i].word
    return df_game_state, definitions


def init_all_dictionaries(dict_folder: str):
    def init_dictionary(sub_dict_folder: str):
        sub_dict = {}
        for i in range(2, 25):
            df_words_file = open(
                f"{DICTIONARY_TO_PATH[sub_dict_folder]}/{sub_dict_folder}/word_{i}.csv",
                "r",
                encoding="utf-8",
            )
            df_words = [x.strip() for x in df_words_file]
            sub_dict[i] = df_words
        return sub_dict

    all_dictionaries = {
        DICTIONARY.CUSTOM_DICTIONARY: init_dictionary(DICTIONARY.CUSTOM_DICTIONARY),
        DICTIONARY.DEFAULT_DICTIONARY: init_dictionary(dict_folder),
    }
    return all_dictionaries


def check_every_definition_has_solution(definitions: list[Definition]) -> bool:
    for definition in definitions:
        if not definition.is_set and definition.possible_values == []:
            return False
    return True


def check_every_definition_is_set(definitions: list[Definition]) -> bool:
    for definition in definitions:
        if not definition.is_set:
            return False
    return True


def enrich_custom_definitions(
    definitions: list[Definition],
) -> tuple[list[Definition], int]:
    score = 0
    df_custom_dictionary = pd.read_csv(
        f"{DICTIONARY_TO_PATH[DICTIONARY.CUSTOM_DICTIONARY]}/{DICTIONARY.CUSTOM_DICTIONARY}.csv",
        dtype=object,
    )
    custom_definition_dictionary = dict(df_custom_dictionary.values)
    for d in definitions:
        # PLACEHOLDER
        d.definition = d.word
        arrowed_place_holder = get_arrowed_place_holder(d.definition_type)
        print(f"({d.i},{d.j}, {arrowed_place_holder.unicode_char}) : {d.word}")
        if d.word in custom_definition_dictionary:
            if not pd.isna(custom_definition_dictionary[d.word]):
                d.definition = custom_definition_dictionary[d.word] or d.definition
            d.is_custom_definition = True
            score += 1
    return definitions, score


def generate_arrow_crossword(dictionary: str, map_file: str):
    pygame.init()

    df_init = pd.read_csv(
        f"resources/maps/{map_file}.csv", dtype=object, sep=",", header=None
    )
    all_dictionaries = init_all_dictionaries(dictionary)
    df_game_state, all_definitions = init_state(df_init, all_dictionaries)

    max_size = len(all_definitions)

    def backtracking(
        definition_index: int, all_definitions, df_game_state, all_dictionaries
    ) -> bool:
        if definition_index == max_size:
            return True
        definition = all_definitions[definition_index]
        if not (definition.is_set):
            while definition.possible_values != [] and definition.nb_tries < THRESHOLD:
                definition.nb_tries += 1
                chosen_word = definition.possible_values.pop()
                definition.is_set = True
                definition.previous_word = definition.word
                definition.word = chosen_word
                # print(f'{definition_index} -> {chosen_word}')
                df_game_state = set_letters(definition, df_game_state)
                all_definitions = update_definitions_from_game_state(
                    all_definitions, df_game_state, all_dictionaries
                )

                if check_every_definition_has_solution(all_definitions):
                    if backtracking(
                        definition_index + 1,
                        all_definitions,
                        df_game_state,
                        all_dictionaries,
                    ):
                        return True

                definition.is_set = False
                definition.word = definition.previous_word
                df_game_state = set_letters(definition, df_game_state)
            return False
        else:
            return backtracking(definition_index + 1, all_definitions, df_game_state)

    backtracking(0, all_definitions, df_game_state, all_dictionaries)
    df_all_definitions = pd.DataFrame(df_game_state)
    print(df_all_definitions)
    if check_every_definition_is_set(all_definitions):
        all_definitions, score = enrich_custom_definitions(all_definitions)
        print(f"SCORE FINAL : {score}")
        save_definitions_to_json(all_definitions, score, map_file)
    else:
        print("NOT ENOUGH")
