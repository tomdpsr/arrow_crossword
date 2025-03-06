import datetime
import json
from dataclasses import dataclass
from random import shuffle

import pandas as pd

from back.arrow_crossword_generation.utilities.generation_utilities import (
    get_forbidden_words,
    get_possible_values_from_all_dic,
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
    h_capelitos: dict[int, list[int]] = None
    v_capelitos: dict[int, list[int]] = None
    linked_capelitos: dict[int, list[int]] = None

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
        self.capelitos = self.shuffle_and_tag_capelitos(opts)

        self.init_capelitos_h_v()
        self.linked_capelitos = {}
        forbidden_words = get_forbidden_words(self.capelitos, validated_custom_words)
        for index, capelito in enumerate(self.capelitos):
            capelito.possible_values = get_possible_values_from_all_dic(
                capelito.word,
                dictionary_hander,
                forbidden_words,
                capelito.is_custom_capelito,
            )
            self.linked_capelitos[index] = self.find_capelitos_to_change(capelito)

        self.link_capelitos_together()
        for i in range(len(self.capelitos)):
            self.capelitos[i].previous_word = self.capelitos[i].word

    def link_capelitos_together(self):
        # Sorry for the n square
        # Only for the capelitos who share the same definition textbox
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

    def init_capelitos_h_v(self):
        self.h_capelitos, self.v_capelitos = {}, {}
        for index, capelito in enumerate(self.capelitos):
            if capelito.arrowed_place_holder.is_horizontal:
                if capelito.get_first_letter_i() not in self.h_capelitos:
                    self.h_capelitos[capelito.get_first_letter_i()] = [index]
                else:
                    self.h_capelitos[capelito.get_first_letter_i()].append(index)
            else:
                if capelito.get_first_letter_j() not in self.v_capelitos:
                    self.v_capelitos[capelito.get_first_letter_j()] = [index]
                else:
                    self.v_capelitos[capelito.get_first_letter_j()].append(index)

    def find_capelitos_to_change(self, capelito: Capelito) -> list[int]:
        capelitos_to_change = []
        for index, letter in enumerate(capelito.word):
            if capelito.arrowed_place_holder.is_horizontal:
                capelito_i = capelito.get_first_letter_i()
                current_letter_j = capelito.get_first_letter_j() + index
                if current_letter_j in self.v_capelitos:
                    for capelito_v in self.v_capelitos[current_letter_j]:
                        capelito_to_update = self.capelitos[capelito_v]
                        if (
                            capelito_to_update.get_first_letter_i()
                            <= capelito_i
                            <= capelito_to_update.get_first_letter_i()
                            + len(capelito_to_update.word)
                            - 1
                        ):
                            if not capelito_to_update.is_set:
                                capelitos_to_change.append(capelito_v)
            else:
                capelito_j = capelito.get_first_letter_j()
                current_letter_i = capelito.get_first_letter_i() + index
                if current_letter_i in self.h_capelitos:
                    for capelito_h in self.h_capelitos[current_letter_i]:
                        capelito_to_update = self.capelitos[capelito_h]
                        if (
                            capelito_to_update.get_first_letter_j()
                            <= capelito_j
                            <= capelito_to_update.get_first_letter_j()
                            + len(capelito_to_update.word)
                            - 1
                        ):
                            if not capelito_to_update.is_set:
                                capelitos_to_change.append(capelito_h)
        return capelitos_to_change

    def shuffle_and_tag_capelitos(self, opts: dict) -> list[Capelito]:
        # We only keep min 3 length words
        custom_capelitos = [d for d in self.capelitos if len(d.word) > 2]
        shuffle(custom_capelitos)
        custom_capelitos = custom_capelitos[: opts["nb_custom_capelitos_min"]]
        for custom_capelito in custom_capelitos:
            custom_capelito.is_custom_capelito = True

        capelitos = [d for d in self.capelitos if d not in custom_capelitos]
        capelitos = sorted(capelitos, key=lambda x: len(x.word), reverse=True)
        return custom_capelitos + capelitos
