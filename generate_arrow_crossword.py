import re
from random import shuffle

import pandas as pd

from utilities.arrowed_definitions import get_arrowed_definition_mapping
from utilities.definition import Definition

THRESHOLD = 10


def get_possibles_values_from_dic(letters, sub_dict: dict):
    r = re.compile(fr'{letters}')
    possible_values = list(filter(r.match, sub_dict[len(letters)]))
    shuffle(possible_values)
    return possible_values

def update_definitions_from_game_state(definitions: list[Definition], df_game_state: list[list[str]], gros_dico: dict) -> list[Definition]:
    for definition in definitions:
        mapp_i_diff = get_arrowed_definition_mapping('i_diff')
        mapp_j_diff = get_arrowed_definition_mapping('j_diff')
        mapp_is_horizontal = get_arrowed_definition_mapping('is_horizontal')
        letters = ''
        i = definition.i + mapp_i_diff[definition.definition_type]
        j = definition.j + mapp_j_diff[definition.definition_type]
        while not (df_game_state[i][j].isnumeric()):
            letters += df_game_state[i][j]
            if mapp_is_horizontal[definition.definition_type]:
                j += 1
            else:
                i += 1
            if j == len(df_game_state[0]) or i == len(df_game_state):
                break
        definition.word = letters

        # get possible values
        if not definition.is_set:
            perso_possible_values = get_possibles_values_from_dic(letters, gros_dico['perso'])
            full_possible_values = get_possibles_values_from_dic(letters, gros_dico['full'])
            definition.possible_values = full_possible_values + perso_possible_values
            definition.nb_tries = 0

    return definitions

def set_letters(definition: Definition, df_game_state: list[list[str]]) -> list[list[str]]:
    mapp_i_diff = get_arrowed_definition_mapping('i_diff')
    mapp_j_diff = get_arrowed_definition_mapping('j_diff')
    mapp_is_horizontal = get_arrowed_definition_mapping('is_horizontal')
    i = definition.i + mapp_i_diff[definition.definition_type]
    j = definition.j + mapp_j_diff[definition.definition_type]
    for l in definition.word:
        df_game_state[i][j] = l
        if mapp_is_horizontal[definition.definition_type]:
            j += 1
        else:
            i += 1
    return df_game_state


def init_state(df_init: pd.DataFrame, gros_dico: dict):
    df_game_state = df_init.values.tolist()
    definitions = []
    for i in range(len(df_game_state)):
        for j in range(len(df_game_state[i])):
            if df_game_state[i][j].isnumeric():
                for digit in df_game_state[i][j]:
                    d = Definition(definition_type=digit,i=i, j=j)
                    definitions.append(d)
    definitions = update_definitions_from_game_state(definitions, df_game_state, gros_dico)
    definitions = sorted(definitions, key=lambda x: len(x.word), reverse=True)
    for i in range(len(definitions)):
        definitions[i].previous_word = definitions[i].word
    return df_game_state, definitions


def init_gros_dico(dict_folder: str):
    def init_dico(sub_dict_folder: str):
        sub_dict = {}
        for i in range(2, 25):
            df_words_file = open(f'resources/dicts/{sub_dict_folder}/mots_{i}.csv', 'r', encoding='utf-8')
            df_words = [x.strip() for x in df_words_file]
            sub_dict[i] = df_words
        return sub_dict

    gros_dico = {}
    gros_dico['perso'] = init_dico('perso')
    gros_dico['full'] = init_dico(dict_folder)
    return gros_dico

def check_every_definition_has_solution(definitions: list[Definition]) -> bool:
    for definition in definitions:
        if not definition.is_set and definition.possible_values == []:
            return False
    return True

def generate_arrow_crossword(dict_folder: str, map_file: str):
    df_init = pd.read_csv(f'resources/maps/{map_file}.csv', dtype=object, sep=',', header=None)
    gros_dico = init_gros_dico(dict_folder)
    df_game_state, definitions = init_state(df_init, gros_dico)

    max_size = len(definitions)

    def backtracking(definition_index: int, definitions, df_game_state, gros_dico) -> bool:
        if definition_index == max_size:
            return True
        definition = definitions[definition_index]
        if not(definition.is_set):
            while definition.possible_values != [] and definition.nb_tries < THRESHOLD:
                definition.nb_tries += 1
                chosen_word = definition.possible_values.pop()
                definition.is_set = True
                definition.previous_word = definition.word
                definition.word = chosen_word
                print(f'{definition_index} -> {chosen_word}')
                df_game_state = set_letters(definition, df_game_state)
                definitions = update_definitions_from_game_state(definitions, df_game_state, gros_dico)

                if check_every_definition_has_solution(definitions):
                    if backtracking(definition_index+1, definitions, df_game_state, gros_dico):
                        return True

                definition.is_set = False
                definition.word = definition.previous_word
                df_game_state = set_letters(definition, df_game_state)
            return False
        else:
            return backtracking(definition_index+1, definitions, df_game_state)


    backtracking(0, definitions, df_game_state, gros_dico)
    df_test = pd.DataFrame(df_game_state)
    print(df_test)
    print('DEFINITIONS')
    ma = get_arrowed_definition_mapping('unicode_char')
    for d in definitions:
        print(f'({d.i},{d.j}, {ma[d.definition_type]}) : {d.word}')
