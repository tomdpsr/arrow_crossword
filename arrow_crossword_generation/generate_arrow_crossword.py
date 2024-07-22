import pandas as pd
import pygame
from loguru import logger

from arrow_crossword_generation.utilities.constants import (
    THRESHOLD,
    DICTIONARY,
)
from arrow_crossword_generation.utilities.generation_utilities import (
    set_letters,
    update_capelitos_from_game_state,
    update_possible_values,
    check_number_capelito_is_set,
)
from arrow_crossword_generation.utilities.init_utilities import (
    init_all_dictionaries,
    get_validated_custom_words,
    init_state,
)
from arrow_crossword_generation.utilities.post_generation_utilities import ( enrich_forbidden_dictionary,
)
from shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword


def generate_arrow_crossword(dictionary: str, map_file: str):
    pygame.init()
    validated_custom_words = get_validated_custom_words()
    arrow_crossword = ArrowCrossword(map_file=map_file)

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
        logger.info(df_all_capelitos)
        arrow_crossword.capelitos = all_capelitos
        arrow_crossword.game_state = df_game_state
        logger.info("End generation of arrow crossword")

    else:
        logger.info("NOT ENOUGH")
    enrich_forbidden_dictionary(all_dictionaries[DICTIONARY.FORBIDDEN_DICTIONARY])
    return arrow_crossword
