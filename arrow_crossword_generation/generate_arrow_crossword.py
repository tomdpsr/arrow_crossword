import pandas as pd
import pygame
from loguru import logger

from arrow_crossword_generation.enrich_mystery_capelito import get_mystery_capelito
from arrow_crossword_generation.utilities.constants import (
    THRESHOLD,
    DICTIONARY,
)
from arrow_crossword_generation.utilities.generation_utilities import (
    set_letters,
    update_capelitos_from_game_state,
    update_possible_values,
    check_number_capelito_is_set,
    clean_custom_possibles_words,
)
from arrow_crossword_generation.utilities.init_utilities import (
    init_all_dictionaries,
    get_validated_custom_words,
    init_state,
)
from arrow_crossword_generation.utilities.post_generation_utilities import (
    enrich_custom_capelitos, enrich_non_custom_capelitos, enrich_forbidden_dictionary,
)
from shared_utilities.capelito.utilities import save_capelitos_to_json


def generate_arrow_crossword(dictionary: str, map_file: str):
    pygame.init()
    validated_custom_words = get_validated_custom_words()

    df_init = pd.read_csv(
        f"resources/maps/{map_file}.csv", dtype=object, sep=",", header=None
    )
    all_dictionaries = init_all_dictionaries(dictionary)
    df_game_state, all_capelitos = init_state(
        df_init, all_dictionaries, validated_custom_words
    )

    max_size = len(all_capelitos)
    logger.info(f'Create arrow crossword for {max_size} capelitos')

    def backtracking(
        capelito_index: int, all_capelitos, df_game_state, all_dictionaries
    ) -> bool:
        if capelito_index == max_size:
            return True
        capelito = all_capelitos[capelito_index]
        if not capelito.is_set:
            while capelito.possible_values != [] and capelito.nb_tries < THRESHOLD:
                capelito.nb_tries += 1
                chosen_word = capelito.possible_values.pop()
                logger.debug(f'{capelito_index}/{max_size} -> {chosen_word} ({capelito.nb_tries})')
                capelito.is_set = True
                capelito.previous_word = capelito.word
                capelito.word = chosen_word
                df_game_state = set_letters(capelito, df_game_state)
                all_capelitos = update_capelitos_from_game_state(
                    all_capelitos, df_game_state
                )
                all_capelitos, every_capelito_has_solution = update_possible_values(
                    all_capelitos, all_dictionaries, validated_custom_words
                )

                if every_capelito_has_solution:
                    if backtracking(
                        capelito_index + 1,
                        all_capelitos,
                        df_game_state,
                        all_dictionaries,
                    ):
                        return True

                capelito.is_set = False
                capelito.word = capelito.previous_word
                df_game_state = set_letters(capelito, df_game_state)
            return False
        else:
            return backtracking(
                capelito_index + 1, all_capelitos, df_game_state, all_dictionaries
            )

    backtracking(0, all_capelitos, df_game_state, all_dictionaries)
    df_all_capelitos = pd.DataFrame(df_game_state)

    if check_number_capelito_is_set(all_capelitos, len(all_capelitos)):
        # get mystery_capelito
        possible_mystery_capelitos = [
            w for ws in all_dictionaries[DICTIONARY.CUSTOM_DICTIONARY].values() for w in ws
        ]
        possible_mystery_capelitos = clean_custom_possibles_words(
            possible_mystery_capelitos, all_capelitos, validated_custom_words
        )
        mystery_capelito = get_mystery_capelito(df_game_state, possible_mystery_capelitos)


        # Enrich capelitos
        logger.info('Enrich capelitos')
        all_capelitos, score, mystery_capelito_definition = enrich_custom_capelitos(all_capelitos, mystery_capelito['word'])
        all_capelitos = enrich_non_custom_capelitos(all_capelitos)

        if mystery_capelito_definition:
            mystery_capelito['definition'] = mystery_capelito_definition
        logger.info(df_all_capelitos)
        logger.info(f"Final Score : {score}")
        logger.info(f"Mystery Capelito : {mystery_capelito['word']}")
        save_capelitos_to_json(
            capelitos=all_capelitos,
            score=score,
            map_file=map_file,
            mystery_capelito=mystery_capelito,
        )
    else:
        logger.info("NOT ENOUGH")
    enrich_forbidden_dictionary(all_dictionaries[DICTIONARY.FORBIDDEN_DICTIONARY])
