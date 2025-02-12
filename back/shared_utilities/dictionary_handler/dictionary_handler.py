import os
from dataclasses import dataclass, field

from back.shared_utilities.dictionary_handler.constants import (
    DICTIONARY,
    DICTIONARY_TO_PATH,
)


@dataclass
class DictionaryHandler:
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
