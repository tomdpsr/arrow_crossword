import os
import re

from loguru import logger

from back.shared_utilities.arrowed_place_holder.arrowed_place_holder import (
    get_arrowed_place_holder,
)
from back.shared_utilities.capelito.capelito import Capelito
from back.shared_utilities.dictionary_handler.dictionary_handler import (
    DictionaryHandler,
)


def set_letters(capelito: Capelito, df_game_state: list[list[str]]) -> list[list[str]]:
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


def check_number_capelito_is_set(capelitos: list[Capelito], n: int) -> bool:
    count = 0
    for capelito in capelitos:
        if capelito.is_set:
            count += 1
    return count == n


def clean_custom_possibles_words(
    custom_possible_words, capelitos, validated_custom_words
):
    set_words = [w.word for w in capelitos]
    possible_words = list(
        (set(custom_possible_words) - set(validated_custom_words)) - set(set_words)
    )
    return possible_words


def get_forbidden_words(capelitos, validated_custom_words: []):
    set_words = [w.word for w in capelitos if w.is_set]
    forbidden_words = list(set(validated_custom_words + set_words))
    return forbidden_words


def get_possibles_values_from_dic(
    letters, sub_dict: dict, forbidden_words=[]
) -> list | None:
    # TODO Add more intelligence : all dots => return set, all letters => no regexp ?
    r = re.compile(rf"{letters}")
    possible_values = list(
        set(filter(r.match, sub_dict[len(letters)])) - set(forbidden_words)
    )
    return possible_values


def get_possible_values_from_all_dic(
    letters, dictionary_hander, forbidden_words, should_be_custom: bool
) -> list[str] | None:

    if letters in dictionary_hander.forbidden_dictionary[len(letters)]:
        return []

    max_size = int(os.environ["NB_MAX_TRIES_PER_WORD"])
    custom_possible_values = get_possibles_values_from_dic(
        letters, dictionary_hander.custom_dictionary, forbidden_words
    )
    if should_be_custom:
        default_possible_values = []
    else:
        default_possible_values = get_possibles_values_from_dic(
            letters,
            dictionary_hander.main_dictionary,
        )
    return (custom_possible_values + default_possible_values)[:max_size]


def update_capelito_word_from_another(
    capelito_to_update: Capelito, capelito_base: Capelito
):
    if capelito_base.arrowed_place_holder.is_horizontal:
        pos_in_word2_base = abs(
            capelito_to_update.get_first_letter_j() - capelito_base.get_first_letter_j()
        )
        pos_in_word_to_update = abs(
            capelito_to_update.get_first_letter_i() - capelito_base.get_first_letter_i()
        )

    else:
        pos_in_word2_base = abs(
            capelito_to_update.get_first_letter_i() - capelito_base.get_first_letter_i()
        )
        pos_in_word_to_update = abs(
            capelito_to_update.get_first_letter_j() - capelito_base.get_first_letter_j()
        )

    word_chars = list(capelito_to_update.word)
    word_chars[pos_in_word_to_update] = capelito_base.word[pos_in_word2_base]
    capelito_to_update.word = "".join(word_chars)

    return capelito_to_update
