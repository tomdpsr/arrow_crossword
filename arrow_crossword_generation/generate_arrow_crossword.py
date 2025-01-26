import os

import pandas as pd
import pygame
from loguru import logger

from arrow_crossword_generation.utilities.generation_utilities import (
    set_letters,
    update_possible_values,
    check_number_capelito_is_set,
)

from arrow_crossword_generation.utilities.post_generation_utilities import (
    enrich_forbidden_dictionary,
)
from shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword
from shared_utilities.dictionary_handler.dictionary_handler import DictionaryHandler
from shared_utilities.utilities import get_validated_custom_words


def generate_arrow_crossword(main_dictionary_folder: str, map_file: str):
    pygame.init()
    opts = {
        'nb_max_tries_per_word': int(os.environ['NB_MAX_TRIES_PER_WORD']),
        'nb_custom_capelitos_min': int(os.environ['NB_CUSTOM_CAPELITOS_MIN'])
    }
    validated_custom_words = get_validated_custom_words()

    dictionary_hander = DictionaryHandler(main_dictionary_folder)

    arrow_crossword = ArrowCrossword(map_file=map_file)
    arrow_crossword.init_state(dictionary_hander, validated_custom_words, opts)



    max_size = len(arrow_crossword.capelitos)
    logger.info(f"Create arrow crossword for {max_size} capelitos")

    def backtracking(
        capelito_index: int,
        arrow_crossword: ArrowCrossword,
        dictionary_hander: DictionaryHandler,
        opts: dict,
    ) -> bool:
        if capelito_index == max_size:
            return True
        capelito = arrow_crossword.capelitos[capelito_index]
        if not capelito.is_set:
            for possible_value in capelito.possible_values:
                capelito.nb_tries += 1
                logger.debug(
                    f"{capelito_index}/{max_size} -> {possible_value} ({capelito.nb_tries})"
                )
                capelito.is_set = True
                capelito.previous_word = capelito.word
                capelito.word = possible_value

                # maybe useless
                arrow_crossword.game_state = set_letters(
                    capelito, arrow_crossword.game_state
                )

                arrow_crossword.update_capelitos_from_game_state()
                arrow_crossword.capelitos, every_capelito_has_solution = (
                    update_possible_values(
                        arrow_crossword.capelitos,
                        dictionary_hander,
                        validated_custom_words,
                        opts
                    )
                )

                if every_capelito_has_solution:
                    if backtracking(
                        capelito_index + 1,
                        arrow_crossword,
                        dictionary_hander,
                        opts
                    ):
                        return True

                capelito.is_set = False
                capelito.word = capelito.previous_word

                # maybe uselsse
                arrow_crossword.df_game_state = set_letters(
                    capelito, arrow_crossword.game_state
                )
            return False
        else:
            return backtracking(capelito_index + 1, arrow_crossword, dictionary_hander, opts)

    backtracking(0, arrow_crossword, dictionary_hander, opts)
    df_all_capelitos = pd.DataFrame(arrow_crossword.game_state)

    if check_number_capelito_is_set(
        arrow_crossword.capelitos, len(arrow_crossword.capelitos)
    ):
        logger.info(df_all_capelitos)
        logger.info("End generation of arrow crossword")

    else:
        logger.info("NOT ENOUGH")
    enrich_forbidden_dictionary(dictionary_hander.forbidden_dictionary)
    return arrow_crossword
