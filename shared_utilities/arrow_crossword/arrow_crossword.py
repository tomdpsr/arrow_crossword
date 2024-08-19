import datetime
import json
from dataclasses import dataclass

from shared_utilities.capelito.capelito import Capelito

@dataclass
class ArrowCrossword:
    filename: str = None
    map_file: str = None
    score: int = None
    date: datetime.datetime = None
    capelitos: list[Capelito] = None
    mystery_capelito: dict = None
    game_state : list[list[str]] = None

    def __post_init__(self):
        if self.filename:
            file = open(f"data/capelitos/{self.filename}.json")
            arrow_crossword = json.load(file)
            all_capelitos = []
            for c in arrow_crossword['capelitos']:
                all_capelitos.append(Capelito(
                    capelito_type=c['capelito_type'],
                    i=c['i'],
                    j=c['j'],
                    word=c['word'],
                    definition=c['definition'],
                    is_custom_capelito=c['is_custom_capelito'],
                ))

            # Sorry for the n square
            for d in all_capelitos:
                if d.linked_capelito is None:
                    for d2 in all_capelitos:
                        if d.i == d2.i and d.j == d2.j and d.word != d2.word:
                            d.linked_capelito, d2.linked_capelito = d2, d
            self.capelitos = all_capelitos

            # Sorry for the ?
            self.map_file = arrow_crossword['map_file']
            self.score = arrow_crossword['score']
            self.date = arrow_crossword['date']
            self.mystery_capelito = arrow_crossword['mystery_capelito']
            self.game_state = arrow_crossword['game_state']

            # useful to return ?
            return arrow_crossword

    def save_arrow_crossword_to_json(
        self,
    ) -> None:
        self.filename = (
            self.filename
            or f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{self.map_file}"
        )
        data_to_export = {
            "map_file": self.map_file,
            "score": self.score,
            "date": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            "capelitos": [d.export_to_dict() for d in self.capelitos],
            "mystery_capelito": self.mystery_capelito,
            "game_state": self.game_state,
        }
        with open(
            f"data/capelitos/{self.filename}.json",
            "w",
        ) as f:
            json.dump(data_to_export, f)
