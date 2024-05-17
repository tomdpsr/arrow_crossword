import pandas as pd

from utilities.arrowed_definitions import get_arrowed_definition_mapping
from utilities.definition import Definition


def get_letters(definition: Definition, df_ll: list[list[str]]) -> Definition:
    mapp_i_diff = get_arrowed_definition_mapping('i_diff')
    mapp_j_diff = get_arrowed_definition_mapping('j_diff')
    mapp_is_horizontal = get_arrowed_definition_mapping('is_horizontal')
    letters = ''
    i = definition.i + mapp_i_diff[definition.definition_type]
    j = definition.j + mapp_j_diff[definition.definition_type]
    while not(df_ll[i][j].isnumeric()):
        letters += df_ll[i][j]
        if mapp_is_horizontal[definition.definition_type]:
            j += 1
        else:
            i += 1
        if j == len(df_ll[0]) or i == len(df_ll):
            break
    definition.word = letters
    return definition

def set_letters(definition: Definition, df_ll: list[list[str]]) -> list[list[str]]:
    mapp_i_diff = get_arrowed_definition_mapping('i_diff')
    mapp_j_diff = get_arrowed_definition_mapping('j_diff')
    mapp_is_horizontal = get_arrowed_definition_mapping('is_horizontal')
    i = definition.i + mapp_i_diff[definition.definition_type]
    j = definition.j + mapp_j_diff[definition.definition_type]
    for l in definition.word:
        df_ll[i][j] = l
        if mapp_is_horizontal[definition.definition_type]:
            j += 1
        else:
            i += 1
    return df_ll


def init_state(df_init: pd.DataFrame):
    df_ll = df_init.values.tolist()
    definitions = []
    for i in range(len(df_ll)):
        for j in range(len(df_ll[i])):
            if df_ll[i][j] != '.':
                d = Definition(definition_type=df_ll[i][j],i=i, j=j)
                d = get_letters(d, df_ll)
                definitions.append(d)
    definitions = sorted(definitions, key=lambda x: len(x.word), reverse=True)
    return df_ll, definitions



if __name__ == "__main__":
    df_init = pd.read_csv('maps/map1.csv', dtype=object, sep=',', header=None)
    df_words = pd.read_csv('dicts/mots_all.csv', dtype=str, sep=',', header=None)

    df_ll, definitions = init_state(df_init)

    whi = True
    # start definitions

    df_def_done = []

    while whi:
        # loop
        for d in definitions:
            d = get_letters(d, df_ll)
            #print(f'Récupération pour def ({d.i},{d.j}) : {d.word}')
            df_sample = df_words[(df_words[0].str.contains(fr'^{d.word}$')) & ~(df_words[0].isin([d2.word for d2 in df_def_done]))]
            if df_sample.empty:
                #print('Aucun mot restant')
                df_ll, definitions = init_state(df_init)
                df_def_done.clear()
                break
            nb_mots = df_sample.size
            df_sample = df_sample.sample(n=1)
            #print(f'Mot récupéré : {df_sample[0].iloc[0]} (sur {nb_mots})')
            d.word = df_sample[0].iloc[0]
            d.is_set = True
            df_ll = set_letters(d, df_ll)

            # check if all mot
            df_def_done = [d3 for d3 in definitions if d3.is_set]
            if len(df_def_done) >= 10:
                print(f'{len(df_def_done)}/{len(definitions)}')
            if len(df_def_done) == len(definitions):
                whi = False

    df_test = pd.DataFrame(df_ll)
    print(df_test)
    print(1)
