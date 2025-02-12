import datetime
import json
from dataclasses import dataclass

import pandas as pd

from back.arrow_crossword_generation.utilities.generation_utilities import (
    shuffle_capelitos,
    update_possible_values,
)
from back.shared_utilities.arrowed_place_holder.arrowed_place_holder import (
    get_arrowed_place_holder,
)
from back.shared_utilities.capelito.capelito import Capelito
from back.shared_utilities.dictionary_handler.dictionary_handler import (
    DictionaryHandler,
)


@dataclass
class ArrowCrossword:
    file_path: str = None
    map_file: str = None
    score: int = None
    date: datetime.datetime = None
    capelitos: list[Capelito] = None
    mystery_capelito: dict = None
    game_state: list[list[str]] = None

    def __post_init__(self):
        if self.file_path:
            file = open(self.file_path)
            arrow_crossword = json.load(file)
            all_capelitos = []
            for c in arrow_crossword["capelitos"]:
                all_capelitos.append(
                    Capelito(
                        capelito_type=c["capelito_type"],
                        i=c["i"],
                        j=c["j"],
                        word=c["word"],
                        definition=c["definition"],
                        is_custom_capelito=c["is_custom_capelito"],
                    )
                )

            self.capelitos = all_capelitos
            self.link_capelitos_together()

            # Sorry for the ?
            self.map_file = arrow_crossword["map_file"]
            self.score = arrow_crossword["score"]
            self.date = arrow_crossword["date"]
            self.mystery_capelito = arrow_crossword["mystery_capelito"]
            self.game_state = arrow_crossword["game_state"]

    def init_state(
        self, dictionary_hander: DictionaryHandler, validated_custom_words, opts: dict
    ):
        df_init = pd.read_csv(
            f"back/resources/maps/{self.map_file}.csv",
            dtype=object,
            sep=",",
            header=None,
        )
        self.game_state = df_init.values.tolist()
        self.capelitos = []
        for i in range(len(self.game_state)):
            for j in range(len(self.game_state[i])):
                if self.game_state[i][j].isnumeric():
                    for digit in self.game_state[i][j]:
                        self.capelitos.append(Capelito(capelito_type=digit, i=i, j=j))
        self.update_capelitos_from_game_state()
        self.capelitos = shuffle_capelitos(self.capelitos, opts)
        self.capelitos, _ = update_possible_values(
            self.capelitos, dictionary_hander, validated_custom_words, opts
        )
        self.link_capelitos_together()
        for i in range(len(self.capelitos)):
            self.capelitos[i].previous_word = self.capelitos[i].word

    def link_capelitos_together(self):
        # Sorry for the n square
        for c in self.capelitos:
            if c.linked_capelito is None:
                for c2 in self.capelitos:
                    if (
                        c.i == c2.i
                        and c.j == c2.j
                        and c.capelito_type != c2.capelito_type
                    ):
                        c.linked_capelito, c2.linked_capelito = c2, c

    def save_arrow_crossword_to_json(
        self,
    ) -> None:
        self.file_path = (
            self.file_path
            or f"data/capelitos/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{self.map_file}.json"
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
            self.file_path,
            "w",
        ) as f:
            json.dump(data_to_export, f)

    def update_capelitos_from_game_state(self):
        for capelito in self.capelitos:
            arrowed_place_holder = get_arrowed_place_holder(capelito.capelito_type)
            letters = ""
            i = capelito.i + arrowed_place_holder.i_diff
            j = capelito.j + arrowed_place_holder.j_diff
            while not (self.game_state[i][j].isnumeric()):
                letters += self.game_state[i][j]
                if arrowed_place_holder.is_horizontal:
                    j += 1
                else:
                    i += 1
                if j == len(self.game_state[0]) or i == len(self.game_state):
                    break
            capelito.word = letters
