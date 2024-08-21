import os
from dataclasses import dataclass, field

from arrow_crossword_generation.utilities.constants import DICTIONARY_TO_PATH
from shared_utilities.dictionary_handler.constants import DICTIONARY


@dataclass
class DictionaryHandler:
    main_dictionary_folder: str
    custom_dictionary: dict = field(init=False)
    main_dictionary: dict = field(init=False)
    forbidden_dictionary: dict = field(init=False)

    def __post_init__(self):
        self.custom_dictionary = self.init_dictionary(DICTIONARY.CUSTOM_DICTIONARY)
        self.main_dictionary = self.init_dictionary(DICTIONARY.MAIN_DICTIONARY)
        self.custom_dictionary = self.init_dictionary(DICTIONARY.CUSTOM_DICTIONARY)

    def init_dictionary(self, sub_dict_folder: str):
        dictionary = {}
        for i in range(2, 25):
            dic_file = f"{DICTIONARY_TO_PATH[sub_dict_folder]}/{sub_dict_folder}/word_{i}.csv"
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
