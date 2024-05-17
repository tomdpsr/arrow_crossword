import re
from random import shuffle

from arrow_crossword_generation.utilities.constants import (
    NB_CUSTOM_DEFINITIONS_MIN,
    DICTIONARY,
)
from shared_utilities.arrowed_place_holder.arrowed_place_holder import (
    get_arrowed_place_holder,
)
from shared_utilities.definition.definition import Definition


def shuffle_definitions(definitions: list[Definition]) -> list[Definition]:
    # We only keep min 3 length words
    custom_definitions = [d for d in definitions if len(d.word) > 2]
    shuffle(custom_definitions)
    custom_definitions = custom_definitions[:NB_CUSTOM_DEFINITIONS_MIN]

    definitions = [d for d in definitions if d not in custom_definitions]
    definitions = sorted(definitions, key=lambda x: len(x.word), reverse=True)
    return custom_definitions + definitions


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


def check_every_definition_has_solution(definitions: list[Definition], definition_index:int) -> bool:
    for d in range(definition_index, len(definitions)):
        if not definitions[d].is_set and not definitions[d].possible_values:
            #print(definitions[d].word)
            return False
    return True


def check_number_definition_is_set(definitions: list[Definition], n: int) -> bool:
    count = 0
    for definition in definitions:
        if definition.is_set:
            count += 1
    return count == n


def update_possible_values(
    definitions: list[Definition],
    all_dictionaries: dict,
    validated_custom_words: list[str],
) -> list[Definition]:
    cursor = 0
    every_definition_has_solution = True
    for definition in definitions:
        cursor += 1
        should_be_custom = (cursor <= NB_CUSTOM_DEFINITIONS_MIN)
        if definition.word in all_dictionaries[DICTIONARY.FORBIDDEN_DICTIONARY][len(definition.word)] and not should_be_custom:
            every_definition_has_solution = False
            break
        # get possible values
        #if not definition.is_set and definition.previous_regexp != definition.word:
        if not definition.is_set:
            custom_possible_values = get_possibles_values_from_dic(
                definition.word, all_dictionaries[DICTIONARY.CUSTOM_DICTIONARY]
            )
            custom_possible_values = clean_custom_possibles_words(
                custom_possible_values, definitions, validated_custom_words
            )
            if should_be_custom:
                default_possible_values = []
            else:
                default_possible_values = get_possibles_values_from_dic(
                    definition.word, all_dictionaries[DICTIONARY.DEFAULT_DICTIONARY]
                )
            definition.possible_values = (
                default_possible_values + custom_possible_values
            )
            definition.nb_tries = 0

            if not definition.possible_values:
                #print(f'{cursor} ---> {definition.word}')
                every_definition_has_solution = False
                if not should_be_custom:
                    #definition.banned_values.add(definition.word)
                    all_dictionaries[DICTIONARY.FORBIDDEN_DICTIONARY][len(definition.word)].add(definition.word)
                break

    return definitions, every_definition_has_solution


def clean_custom_possibles_words(
    custom_possible_words, definitions, validated_custom_words
):
    set_words = [
        w.word for w in definitions
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


def update_definitions_from_game_state(
    definitions: list[Definition],
    df_game_state: list[list[str]],
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
        #definition.previous_regexp = definition.word
        definition.word = letters
    return definitions
