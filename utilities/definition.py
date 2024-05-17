from dataclasses import dataclass


@dataclass
class Definition:
    definition_type: str
    i: int
    j: int
    word: str = ''
    is_set: bool = False

