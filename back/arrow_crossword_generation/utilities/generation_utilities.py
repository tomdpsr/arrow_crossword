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
#from shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword





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


def check_every_capelito_has_solution(
    capelitos: list[Capelito], capelito_index: int
) -> bool:
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
        dictionary_hander: DictionaryHandler,
        validated_custom_words: list[str],
) -> tuple[list[Capelito], bool]:
    for index, capelito in enumerate(capelitos, 1):
        word_length = len(capelito.word)

        if not capelito.is_custom_capelito and capelito.word in dictionary_hander.forbidden_dictionary[word_length]:
            logger.debug(f"forbidden - {index} ---> {capelito.word}")
            return capelitos, False

        if not capelito.is_set:
            forbidden_words = get_forbidden_words(capelitos, validated_custom_words)
            capelito.possible_values = get_possible_values_from_all_dic(
                capelito.word, dictionary_hander, forbidden_words, capelito.is_custom_capelito
            )
            capelito.nb_tries = 0

            if capelito.possible_values is None:
                logger.debug(f"{index} ---> {capelito.word}")
                if not capelito.is_custom_capelito:
                    dictionary_hander.forbidden_dictionary[word_length].add(capelito.word)
                return capelitos, False

    return capelitos, True


def clean_custom_possibles_words(
    custom_possible_words, capelitos, validated_custom_words
):
    set_words = [w.word for w in capelitos]
    possible_words = list(
        (set(custom_possible_words) - set(validated_custom_words)) - set(set_words)
    )
    return possible_words



def get_forbidden_words(capelitos, validated_custom_words):
    set_words = [w.word for w in capelitos if w.is_set]
    forbidden_words = list(set(validated_custom_words + set_words))
    return forbidden_words


def get_possibles_values_from_dic(
    letters, sub_dict: dict, forbidden_words=[]
) -> list | None:
    r = re.compile(rf"{letters}")
    possible_values = list(
        set(filter(r.match, sub_dict[len(letters)])) - set(forbidden_words)
    )
    return possible_values

def get_possible_values_from_all_dic(
    letters, dictionary_hander, forbidden_words, should_be_custom: bool
) -> list[str] | None:
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


def find_capelitos_to_change(
    capelito: Capelito, arrow_crossword
) -> list[int]:
    capelitos_to_change = []
    for index, letter in enumerate(capelito.word):
        if capelito.arrowed_place_holder.is_horizontal:
            capelito_i = capelito.get_first_letter_i()
            current_letter_j = capelito.get_first_letter_j() + index
            if current_letter_j in arrow_crossword.v_capelitos:
                for capelito_v in arrow_crossword.v_capelitos[current_letter_j]:
                    capelito_to_update = arrow_crossword.capelitos[capelito_v]
                    if capelito_to_update.get_first_letter_i() <= capelito_i <= capelito_to_update.get_first_letter_i() + len(
                            capelito_to_update.word) - 1:
                        if not capelito_to_update.is_set:
                            capelitos_to_change.append(capelito_v)
        else:
            capelito_j = capelito.get_first_letter_j()
            current_letter_i = capelito.get_first_letter_i() + index
            if current_letter_i in arrow_crossword.h_capelitos:
                for capelito_h in arrow_crossword.h_capelitos[current_letter_i]:
                    capelito_to_update = arrow_crossword.capelitos[capelito_h]
                    if capelito_to_update.get_first_letter_j() <= capelito_j <= capelito_to_update.get_first_letter_j() + len(
                            capelito_to_update.word) - 1:
                        if not capelito_to_update.is_set:
                            capelitos_to_change.append(capelito_h)
    return capelitos_to_change

def update_capelito_word_from_another(
        capelito_to_update, capelito_base
):
    if capelito_base.arrowed_place_holder.is_horizontal:
        pos_in_word2_base = abs(capelito_to_update.get_first_letter_j() - capelito_base.get_first_letter_j())
        pos_in_word_to_update = abs(capelito_to_update.get_first_letter_i() - capelito_base.get_first_letter_i())

    else:
        pos_in_word2_base = abs(capelito_to_update.get_first_letter_i() - capelito_base.get_first_letter_i())
        pos_in_word_to_update = abs(capelito_to_update.get_first_letter_j() - capelito_base.get_first_letter_j())

    word_chars = list(capelito_to_update.word)
    word_chars[pos_in_word_to_update] = capelito_base.word[pos_in_word2_base]
    capelito_to_update.word = ''.join(word_chars)

    return capelito_to_update