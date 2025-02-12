import copy
from collections import namedtuple
from random import shuffle

import pandas as pd
from loguru import logger

from back.arrow_crossword_generation.create_dictionary import clean_dictionary
from back.arrow_crossword_generation.utilities.generation_utilities import (
    clean_custom_possibles_words,
)
from back.shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword
from back.shared_utilities.dictionary_handler.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
)
from back.shared_utilities.utilities import get_validated_custom_words

MysteryLetter = namedtuple(
    "MysteryLetter",
    [
        "letter",
        "i",
        "j",
    ],
)


def pick_a_custom_word_from_state(available_custom_words, letters):
    magazine_letters = {}

    # Iterate through the magazine and count characters
    for l in letters:
        if l.letter not in magazine_letters:
            magazine_letters[l.letter] = [l]
        else:
            magazine_letters[l.letter] += [l]

    for acw in available_custom_words:
        copy_magazine = copy.deepcopy(magazine_letters)
        word_letters = []
        for char in acw:
            if char in copy_magazine and len(copy_magazine[char]) > 0:
                word_letters.append(copy_magazine[char].pop())
                copy_magazine = sort_dict_by_unused_words(copy_magazine, word_letters)
            else:
                break
        if len(word_letters) == len(acw):
            return word_letters
    return []


def sort_dict_by_unused_words(magazine_letters, word_letters):
    i_already_used = [wl.i for wl in word_letters]
    j_already_used = [wl.j for wl in word_letters]
    for key, value in magazine_letters.items():
        # key is False if its coordinates are never used before, so sorted last for pop()
        value.sort(
            key=lambda x: (x.i in i_already_used) or (x.j in j_already_used),
            reverse=True,
        )
    return magazine_letters


def enrich_mystery_capelito_2(
    arrow_crossword: ArrowCrossword, custom_possible_words: list[str]
) -> ArrowCrossword:
    letters = []
    for i in range(len(arrow_crossword.game_state)):
        for j in range(len(arrow_crossword.game_state[i])):
            if not arrow_crossword.game_state[i][j].isnumeric():
                letters.append(
                    MysteryLetter(letter=arrow_crossword.game_state[i][j], i=i, j=j)
                )

    shuffle(custom_possible_words)

    word_letters = pick_a_custom_word_from_state(custom_possible_words, letters)
    word = "".join([l.letter for l in word_letters])
    arrow_crossword.mystery_capelito = {
        "word": word,
        "word_letters": word_letters,
        "definition": word,
    }

    return arrow_crossword


def enrich_mystery_capelito(arrow_crossword: ArrowCrossword) -> ArrowCrossword:
    logger.info("Enrichment of Mystery Capelito is starting...")
    validated_custom_words = get_validated_custom_words()
    df_words_file = pd.read_csv(
        f"{DICTIONARY_TO_PATH[DICTIONARY.CUSTOM_DICTIONARY]}/{DICTIONARY.CUSTOM_DICTIONARY}.csv",
        dtype=object,
    )
    df_words_file = clean_dictionary(df_words_file)
    custom_possible_words = df_words_file["word"].to_list()

    custom_possible_words = clean_custom_possibles_words(
        custom_possible_words, arrow_crossword.capelitos, validated_custom_words
    )

    arrow_crossword = enrich_mystery_capelito_2(arrow_crossword, custom_possible_words)
    logger.info(
        f'Found word {arrow_crossword.mystery_capelito["word"]} for mystery capelito'
    )

    return arrow_crossword
