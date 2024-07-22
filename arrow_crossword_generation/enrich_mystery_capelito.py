import copy
import json
from collections import namedtuple
from random import shuffle

import pandas as pd

from arrow_crossword_generation.create_dictionary import clean_dictionary
from arrow_crossword_generation.utilities.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
)
from arrow_crossword_generation.utilities.generation_utilities import (
    clean_custom_possibles_words,
    set_letters,
)
from arrow_crossword_generation.utilities.init_utilities import (
    get_validated_custom_words,
)
from shared_utilities.capelito.utilities import (
    save_capelitos_to_json,
    init_capelitos,
)

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
        value.sort(key=lambda x: (x.i in i_already_used) or (x.j in j_already_used), reverse=True)
    return magazine_letters

def get_mystery_capelito(df_game_state, custom_possible_words) -> dict:
    letters = []
    for i in range(len(df_game_state)):
        for j in range(len(df_game_state[i])):
            if not df_game_state[i][j].isnumeric():
                letters.append(MysteryLetter(letter=df_game_state[i][j], i=i, j=j))

    shuffle(custom_possible_words)

    word_letters = pick_a_custom_word_from_state(custom_possible_words, letters)
    word = "".join([l.letter for l in word_letters])
    custom_word_to_export = {
        "word": word,
        "word_letters": word_letters,
        "definition": word,
    }

    return custom_word_to_export


def enrich_mystery_capelito(capelito_filename: str):
    f = open(f"data/capelitos/{capelito_filename}.json")
    filled_map_json = json.load(f)
    capelitos = init_capelitos(filled_map_json)
    df_map = pd.read_csv(
        f"resources/maps/{filled_map_json["map_file"]}.csv", header=None, sep=","
    )
    df_game_state = df_map.values.tolist()
    for capelito in capelitos:
        df_game_state = set_letters(capelito, df_game_state)

    validated_custom_words = get_validated_custom_words()

    df_words_file = pd.read_csv(
        f"{DICTIONARY_TO_PATH[DICTIONARY.CUSTOM_DICTIONARY]}/{DICTIONARY.CUSTOM_DICTIONARY}.csv",
        dtype=object,
    )
    df_words_file = clean_dictionary(df_words_file)
    custom_possible_words = df_words_file["word"].to_list()

    custom_possible_words = clean_custom_possibles_words(
        custom_possible_words, capelitos, validated_custom_words
    )

    custom_word_to_export = get_mystery_capelito(df_game_state, custom_possible_words)

    save_capelitos_to_json(
        capelitos=capelitos,
        score=filled_map_json["score"],
        map_file=filled_map_json["map_file"],
        capelito_file=capelito_filename,
        mystery_capelito=custom_word_to_export,
    )
