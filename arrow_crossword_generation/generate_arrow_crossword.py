import pandas as pd
import pygame

from arrow_crossword_generation.enrich_mystery_word import get_mystery_word
from arrow_crossword_generation.utilities.constants import (
    THRESHOLD,
    DICTIONARY,
)
from arrow_crossword_generation.utilities.generation_utilities import (
    set_letters,
    update_definitions_from_game_state,
    update_possible_values,
    check_number_definition_is_set,
    clean_custom_possibles_words,
)
from arrow_crossword_generation.utilities.init_utilities import (
    init_all_dictionaries,
    get_validated_custom_words,
    init_state,
)
from arrow_crossword_generation.utilities.post_generation_utilities import (
    enrich_custom_definitions, enrich_non_custom_definitions, enrich_forbidden_dictionary,
)
from shared_utilities.definition.utilities import save_definitions_to_json


def generate_arrow_crossword(dictionary: str, map_file: str):
    pygame.init()
    validated_custom_words = get_validated_custom_words()

    df_init = pd.read_csv(
        f"resources/maps/{map_file}.csv", dtype=object, sep=",", header=None
    )
    all_dictionaries = init_all_dictionaries(dictionary)
    df_game_state, all_definitions = init_state(
        df_init, all_dictionaries, validated_custom_words
    )

    max_size = len(all_definitions)
    print(f'Create arrow crossword for {max_size} definitions')

    def backtracking(
        definition_index: int, all_definitions, df_game_state, all_dictionaries
    ) -> bool:
        if definition_index == max_size:
            return True
        definition = all_definitions[definition_index]
        if not definition.is_set:
            while definition.possible_values != [] and definition.nb_tries < THRESHOLD:
                definition.nb_tries += 1
                chosen_word = definition.possible_values.pop()
                #print(f'{definition_index}/{max_size} -> {chosen_word} ({definition.nb_tries})')
                definition.is_set = True
                definition.previous_word = definition.word
                definition.word = chosen_word
                df_game_state = set_letters(definition, df_game_state)
                all_definitions = update_definitions_from_game_state(
                    all_definitions, df_game_state
                )
                all_definitions, every_definition_has_solution = update_possible_values(
                    all_definitions, all_dictionaries, validated_custom_words
                )

                #if check_every_definition_has_solution(all_definitions, definition_index):
                if every_definition_has_solution:
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
            return backtracking(
                definition_index + 1, all_definitions, df_game_state, all_dictionaries
            )

    backtracking(0, all_definitions, df_game_state, all_dictionaries)
    df_all_definitions = pd.DataFrame(df_game_state)

    if check_number_definition_is_set(all_definitions, len(all_definitions)):
        # get mystery_word
        possible_mystery_words = [
            w for ws in all_dictionaries[DICTIONARY.CUSTOM_DICTIONARY].values() for w in ws
        ]
        possible_mystery_words = clean_custom_possibles_words(
            possible_mystery_words, all_definitions, validated_custom_words
        )
        mystery_word = get_mystery_word(df_game_state, possible_mystery_words)


        # Enrich definitions
        print('Enrich definitions')
        all_definitions, score, mystery_definition = enrich_custom_definitions(all_definitions, mystery_word['word'])
        all_definitions = enrich_non_custom_definitions(all_definitions)

        mystery_word['definition'] = mystery_definition
        print(df_all_definitions)
        print(f"SCORE FINAL : {score}")
        print(f"Mot mystere : {mystery_word['word']}")
        save_definitions_to_json(
            definitions=all_definitions,
            score=score,
            map_file=map_file,
            mystery_word=mystery_word,
        )
    else:
        print("NOT ENOUGH")
    enrich_forbidden_dictionary(all_dictionaries[DICTIONARY.FORBIDDEN_DICTIONARY])
