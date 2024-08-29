import os

from back.shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword


def get_validated_custom_words() -> list:
    validated_custom_words = []
    for file in os.listdir("data/validated_capelitos"):
        if file.endswith(".json"):
            arrow_crossword = ArrowCrossword(
                file_path=f"data/validated_capelitos/{file}"
            )
            all_custom_words = [
                w.word for w in arrow_crossword.capelitos if w.is_custom_capelito
            ]
            validated_custom_words = list(
                set(
                    validated_custom_words
                    + all_custom_words
                    + [arrow_crossword.mystery_capelito["word"]]
                )
            )
    return validated_custom_words
