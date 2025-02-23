import os

import pandas as pd
import pygame
from loguru import logger

from back.arrow_crossword_generation.utilities.generation_utilities import (
    check_number_capelito_is_set, find_capelitos_to_change, update_capelito_word_from_another, get_forbidden_words,
    get_possible_values_from_all_dic,
)

from back.arrow_crossword_generation.utilities.post_generation_utilities import (
    enrich_forbidden_dictionary,
)
from back.shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword
from back.shared_utilities.dictionary_handler.dictionary_handler import (
    DictionaryHandler,
)
from back.shared_utilities.utilities import get_validated_custom_words


def generate_arrow_crossword(main_dictionary_folder: str, map_file: str):
    pygame.init()
    opts = {
        "nb_max_tries_per_word": int(os.environ["NB_MAX_TRIES_PER_WORD"]),
        "nb_custom_capelitos_min": int(os.environ["NB_CUSTOM_CAPELITOS_MIN"]),
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
            while (
                capelito.possible_values != []
                and capelito.nb_tries < opts["nb_max_tries_per_word"]
            ):
                capelito.is_set = True
                every_capelito_has_solution = True
                capelito.nb_tries += 1
                chosen_word = capelito.possible_values.pop()
                logger.debug(
                    f"{capelito_index}/{max_size} -> {chosen_word} ({capelito.nb_tries})"
                )
                capelito.previous_word = capelito.word
                capelito.word = chosen_word

                for nb_capelito_to_change in arrow_crossword.linked_capelitos[capelito_index]:
                    capelito_to_change = arrow_crossword.capelitos[nb_capelito_to_change]
                    if not capelito_to_change.is_set:
                        capelito_to_change = update_capelito_word_from_another(capelito_to_change, capelito)
                        forbidden_words = get_forbidden_words(arrow_crossword.capelitos, validated_custom_words)
                        capelito_to_change.possible_values = get_possible_values_from_all_dic(
                            capelito_to_change.word, dictionary_hander, forbidden_words, capelito_to_change.is_custom_capelito
                        )
                        if not capelito_to_change.possible_values:
                            every_capelito_has_solution = False
                            break

                if every_capelito_has_solution:
                    if backtracking(capelito_index + 1, arrow_crossword, dictionary_hander, opts):
                        return True
                else:
                    capelito.word = capelito.previous_word

            # Reinitalize capelito
            capelito.is_set = False

            for nb_capelito_to_change in arrow_crossword.linked_capelitos[capelito_index]:
                if not arrow_crossword.capelitos[nb_capelito_to_change].is_set:
                    arrow_crossword.capelitos[nb_capelito_to_change] = update_capelito_word_from_another(arrow_crossword.capelitos[nb_capelito_to_change], capelito)

            return False
        else:
            return backtracking(
                capelito_index + 1, arrow_crossword, dictionary_hander, opts
            )

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
