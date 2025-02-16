import os
import pickle
from dataclasses import dataclass, field
from typing import Iterator

from back.shared_utilities.dictionary_handler.constants import (
    DICTIONARY,
    DICTIONARY_TO_PATH,
)
from shared_utilities.dictionary_handler.radix_tree import RadixTree
from loguru import logger


class DictionaryHandler:
    def __init__(self, main_dictionary_folder: str):
        logger.info(f"Loading dictionaries from {DICTIONARY.CUSTOM_DICTIONARY}")
        self.custom_trees = self.load_dictionary(DICTIONARY.CUSTOM_DICTIONARY)  # {length: RadixTree}
        logger.info(f"Loading dictionaries from {main_dictionary_folder}")
        self.main_trees = self.load_dictionary(main_dictionary_folder)  # {length: RadixTree}
        logger.info(f"Loading dictionaries from {DICTIONARY.FORBIDDEN_DICTIONARY}")
        self.forbidden_trees = self.load_dictionary(DICTIONARY.FORBIDDEN_DICTIONARY)  # {length: RadixTree}

    @staticmethod
    def load_dictionary(sub_dict_folder: str) -> dict:
        dictionary = {}
        for i in range(2, 25):
            logger.debug(f"Loading dictionary for words of length {i}")
            radix_tree = RadixTree()
            dic_file = os.path.join(DICTIONARY_TO_PATH[sub_dict_folder], sub_dict_folder, f"word_{i}.csv")
            if os.path.isfile(dic_file):
                with open(dic_file, 'r', encoding='utf-8') as f:
                    words = [word.strip() for word in f.readlines() if word.strip()]
            for word in words:
                radix_tree.insert(word)
            dictionary[i] = radix_tree
        return dictionary

    def get_possible_values_from_dic(self, pattern: str, trees: dict[int, RadixTree], forbidden_words: list[str]) -> \
            list[str]:
        length = len(pattern)
        if length not in trees:
            return []

        # Add forbidden words temporarily
        for word in forbidden_words:
            if len(word) == length:
                trees[length].forbidden.add(word)

        # Get matches using pattern
        matches = trees[length].find_matches(pattern)

        # Remove temporary forbidden words
        for word in forbidden_words:
            if len(word) == length:
                trees[length].forbidden.discard(word)

        return matches

    def get_possible_values_from_all_dic(
            self,
            pattern: str,
            forbidden_words: list[str],
            should_be_custom: bool
    ) -> Iterator[str] | None:
        max_size = int(os.environ["NB_MAX_TRIES_PER_WORD"])

        custom_possible_values = self.get_possible_values_from_dic(
            pattern, self.custom_trees, forbidden_words
        )
        if not custom_possible_values:
            return None

        if should_be_custom:
            return iter(custom_possible_values[:max_size])

        default_possible_values = self.get_possible_values_from_dic(
            pattern,
            self.main_trees,
            forbidden_words
        )
        if not default_possible_values:
            return None

        combined_values = custom_possible_values + default_possible_values
        return iter(combined_values[:max_size])


# old
@dataclass
class OldDictionaryHandler:
    main_dictionary_folder: str
    custom_dictionary: dict = field(init=False)
    main_dictionary: dict = field(init=False)
    forbidden_dictionary: dict = field(init=False)

    def __post_init__(self):
        self.custom_dictionary = self.init_dictionary(DICTIONARY.CUSTOM_DICTIONARY)
        self.main_dictionary = self.init_dictionary(self.main_dictionary_folder)
        self.forbidden_dictionary = self.init_dictionary(
            DICTIONARY.FORBIDDEN_DICTIONARY
        )

    @staticmethod
    def init_dictionary(sub_dict_folder: str) -> dict:
        dictionary = {}
        for i in range(2, 25):
            dic_file = (
                f"{DICTIONARY_TO_PATH[sub_dict_folder]}/{sub_dict_folder}/word_{i}.csv"
            )
            if os.path.isfile(dic_file):
                df_words_file = open(
                    f"{DICTIONARY_TO_PATH[sub_dict_folder]}/{sub_dict_folder}/word_{i}.csv",
                    "r",
                    encoding="utf-8",
                )
                df_words = set([x.strip() for x in df_words_file])
            else:
                df_words = set()
            dictionary[i] = df_words
        return dictionary
