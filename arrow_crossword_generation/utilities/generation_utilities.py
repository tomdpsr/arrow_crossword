import re
from random import shuffle

from loguru import logger

from arrow_crossword_generation.utilities.constants import (
    NB_CUSTOM_capelitoS_MIN,
    DICTIONARY,
)
from shared_utilities.arrowed_place_holder.arrowed_place_holder import (
    get_arrowed_place_holder,
)
from shared_utilities.capelito.capelito import Capelito


def shuffle_capelitos(capelitos: list[Capelito]) -> list[Capelito]:
    # We only keep min 3 length words
    custom_capelitos = [d for d in capelitos if len(d.word) > 2]
    shuffle(custom_capelitos)
    custom_capelitos = custom_capelitos[:NB_CUSTOM_capelitoS_MIN]

    capelitos = [d for d in capelitos if d not in custom_capelitos]
    capelitos = sorted(capelitos, key=lambda x: len(x.word), reverse=True)
    return custom_capelitos + capelitos


def set_letters(
    capelito: Capelito, df_game_state: list[list[str]]
) -> list[list[str]]:
    arrowed_place_holder = get_arrowed_place_holder(capelito.capelito_type)
    i = capelito.i + arrowed_place_holder.i_diff
    j = capelito.j + arrowed_place_holder.j_diff
    for l in capelito.word:
        df_game_state[i][j] = l
        if arrowed_place_holder.is_horizontal:
            j += 1
        else:
            i += 1
    return df_game_state


def check_every_capelito_has_solution(capelitos: list[Capelito], capelito_index:int) -> bool:
    for d in range(capelito_index, len(capelitos)):
        if not capelitos[d].is_set and not capelitos[d].possible_values:
            logger.debug(capelitos[d].word)
            return False
    return True


def check_number_capelito_is_set(capelitos: list[Capelito], n: int) -> bool:
    count = 0
    for capelito in capelitos:
        if capelito.is_set:
            count += 1
    return count == n


def update_possible_values(
    capelitos: list[Capelito],
    all_dictionaries: dict,
    validated_custom_words: list[str],
) -> list[Capelito]:
    cursor = 0
    every_capelito_has_solution = True
    for capelito in capelitos:
        cursor += 1
        should_be_custom = (cursor <= NB_CUSTOM_capelitoS_MIN)
        if capelito.word in all_dictionaries[DICTIONARY.FORBIDDEN_DICTIONARY][len(capelito.word)] and not should_be_custom:
            every_capelito_has_solution = False
            break
        # get possible values
        #if not capelito.is_set and capelito.previous_regexp != capelito.word:
        if not capelito.is_set:
            custom_possible_values = get_possibles_values_from_dic(
                capelito.word, all_dictionaries[DICTIONARY.CUSTOM_DICTIONARY]
            )
            custom_possible_values = clean_custom_possibles_words(
                custom_possible_values, capelitos, validated_custom_words
            )
            if should_be_custom:
                default_possible_values = []
            else:
                default_possible_values = get_possibles_values_from_dic(
                    capelito.word, all_dictionaries[DICTIONARY.DEFAULT_DICTIONARY]
                )
            capelito.possible_values = (
                default_possible_values + custom_possible_values
            )
            capelito.nb_tries = 0

            if not capelito.possible_values:
                logger.debug(f'{cursor} ---> {capelito.word}')
                every_capelito_has_solution = False
                if not should_be_custom:
                    all_dictionaries[DICTIONARY.FORBIDDEN_DICTIONARY][len(capelito.word)].add(capelito.word)
                break

    return capelitos, every_capelito_has_solution


def clean_custom_possibles_words(
    custom_possible_words, capelitos, validated_custom_words
):
    set_words = [
        w.word for w in capelitos
    ]
    possible_words = list(
        (set(custom_possible_words) - set(validated_custom_words)) - set(set_words)
    )
    return possible_words

def get_possibles_values_from_dic(letters, sub_dict: dict) -> list:
    r = re.compile(rf"{letters}")
    possible_values = list(filter(r.match, sub_dict[len(letters)]))
    shuffle(possible_values)
    return possible_values


def update_capelitos_from_game_state(
    capelitos: list[Capelito],
    df_game_state: list[list[str]],
) -> list[Capelito]:
    for capelito in capelitos:
        arrowed_place_holder = get_arrowed_place_holder(capelito.capelito_type)
        letters = ""
        i = capelito.i + arrowed_place_holder.i_diff
        j = capelito.j + arrowed_place_holder.j_diff
        while not (df_game_state[i][j].isnumeric()):
            letters += df_game_state[i][j]
            if arrowed_place_holder.is_horizontal:
                j += 1
            else:
                i += 1
            if j == len(df_game_state[0]) or i == len(df_game_state):
                break
        capelito.word = letters
    return capelitos
