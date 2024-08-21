class DICTIONARY:
    CUSTOM_DICTIONARY = "custom_dictionary"
    MAIN_DICTIONARY = "main_dictionary"
    FORBIDDEN_DICTIONARY = "forbidden_dictionary"

    FRENCH_DICTIONARY = "french_dictionary"
    USITO_DICTIONARY = "usito_dictionary"
    FULL_DICTIONARY = "full_dictionary"


DICTIONARY_TO_PATH = {
    DICTIONARY.CUSTOM_DICTIONARY: "data/" + DICTIONARY.CUSTOM_DICTIONARY,
    DICTIONARY.FORBIDDEN_DICTIONARY: "data/" + DICTIONARY.FORBIDDEN_DICTIONARY,
    DICTIONARY.MAIN_DICTIONARY: "resources/dictionaries",
    DICTIONARY.FRENCH_DICTIONARY: "resources/dictionaries",
    DICTIONARY.USITO_DICTIONARY: "resources/dictionaries",
    DICTIONARY.FULL_DICTIONARY: "resources/dictionaries",
}