from loguru import logger

from back.arrow_crossword_generation.utilities.post_generation_utilities import (
    enrich_non_custom_capelitos,
    find_and_enrich_custom_capelitos,
)
from back.shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword


def enrich_arrow_crossword_definition(
    arrow_crossword: ArrowCrossword,
) -> ArrowCrossword:
    logger.info("Enrich custom definitions")
    arrow_crossword = find_and_enrich_custom_capelitos(arrow_crossword)
    logger.info("Enrich non-custom definitions with openai")
    arrow_crossword = enrich_non_custom_capelitos(arrow_crossword)
    logger.info("End enrichment of definitions")

    return arrow_crossword
