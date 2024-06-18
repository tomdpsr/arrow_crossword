from dataclasses import dataclass


@dataclass
class Definition:
    definition_type: str
    i: int
    j: int
    word: str = ''
    previous_word: str = ''
    is_set: bool = False
    possible_values = []
    nb_values: int = 0
    nb_tries: int = 0


