# DICTIONARIES


class DICTIONARY:
    CUSTOM_DICTIONARY = "custom_dictionary"
    DEFAULT_DICTIONARY = "default_dictionary"

    FRENCH_DICTIONARY = "french_dictionary"
    USITO_DICTIONARY = "usito_dictionary"


DICTIONARY_TO_PATH = {
    DICTIONARY.CUSTOM_DICTIONARY: "data/" + DICTIONARY.CUSTOM_DICTIONARY,
    DICTIONARY.DEFAULT_DICTIONARY: "resources/dictionaries",
    DICTIONARY.FRENCH_DICTIONARY: "resources/dictionaries",
    DICTIONARY.USITO_DICTIONARY: "resources/dictionaries",
}

THRESHOLD = 1000
