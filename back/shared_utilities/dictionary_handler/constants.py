from shared_utilities.constants import DATA_FOLDER


class DICTIONARY:
    CUSTOM_DICTIONARY = "custom_dictionary"
    MAIN_DICTIONARY = "main_dictionary"
    FORBIDDEN_DICTIONARY = "forbidden_dictionary"

    FRENCH_DICTIONARY = "french_dictionary"
    USITO_DICTIONARY = "usito_dictionary"
    FULL_DICTIONARY = "full_dictionary"

RESOURCE_DICTIONARIES_FOLDER = "back/resources/dictionaries"

DICTIONARY_TO_PATH = {
    DICTIONARY.CUSTOM_DICTIONARY: DATA_FOLDER + DICTIONARY.CUSTOM_DICTIONARY,
    DICTIONARY.FORBIDDEN_DICTIONARY: DATA_FOLDER + DICTIONARY.FORBIDDEN_DICTIONARY,
    DICTIONARY.MAIN_DICTIONARY: RESOURCE_DICTIONARIES_FOLDER,
    DICTIONARY.FRENCH_DICTIONARY: RESOURCE_DICTIONARIES_FOLDER,
    DICTIONARY.USITO_DICTIONARY: RESOURCE_DICTIONARIES_FOLDER,
    DICTIONARY.FULL_DICTIONARY: RESOURCE_DICTIONARIES_FOLDER,
}


letter_to_score = {
    "A": 1,
    "E": 1,
    "I": 1,
    "L": 1,
    "N": 1,
    "O": 1,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "D": 2,
    "G": 2,
    "M": 2,
    "B": 3,
    "C": 3,
    "P": 3,
    "F": 4,
    "H": 4,
    "V": 4,
    "J": 8,
    "Q": 8,
    "K": 10,
    "W": 10,
    "X": 10,
    "Y": 10,
    "Z": 10,
}
