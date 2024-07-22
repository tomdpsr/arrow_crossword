import json

import pandas as pd
from loguru import logger
from openai import OpenAI

from arrow_crossword_generation.utilities.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
)
from shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword
from shared_utilities.arrowed_place_holder.arrowed_place_holder import get_arrowed_place_holder
from shared_utilities.capelito.capelito import Capelito


def find_and_enrich_custom_capelitos(
    arrow_crossword: ArrowCrossword,
) -> ArrowCrossword:
    arrow_crossword.score = 0
    df_custom_dictionary = pd.read_csv(
        f"{DICTIONARY_TO_PATH[DICTIONARY.CUSTOM_DICTIONARY]}/{DICTIONARY.CUSTOM_DICTIONARY}.csv",
        dtype=object,
    )
    custom_capelito_dictionary = dict(df_custom_dictionary.values)
    for c in arrow_crossword.capelitos:
        custom_char = ''
        if c.word in custom_capelito_dictionary:
            if not pd.isna(custom_capelito_dictionary[c.word]):
                c.definition = custom_capelito_dictionary[c.word] or c.word
            c.is_custom_capelito = True
            arrow_crossword.score += 1
            custom_char = '###'

        arrowed_place_holder = get_arrowed_place_holder(c.capelito_type)
        logger.debug(f"{custom_char}({c.i},{c.j}, {arrowed_place_holder.unicode_char}) : {c.word}")

    # mystery word
    if arrow_crossword.mystery_capelito:
        if not pd.isna(custom_capelito_dictionary[arrow_crossword.mystery_capelito['word']]):
            arrow_crossword.mystery_capelito['definition'] = custom_capelito_dictionary[arrow_crossword.mystery_capelito['word']] or arrow_crossword.mystery_capelito['word']
    return arrow_crossword


def enrich_forbidden_dictionary(forbidden_dictionary: dict):
    for k, v in forbidden_dictionary.items():
        forbidden_l = list(v)
        forbidden_df = pd.DataFrame(forbidden_l, columns=["word"])
        forbidden_df["word"].to_csv(
            f"{DICTIONARY_TO_PATH[DICTIONARY.FORBIDDEN_DICTIONARY]}/{DICTIONARY.FORBIDDEN_DICTIONARY}/word_{k}.csv",
            sep=",",
            index=False,
            header=False,
        )

def get_open_ai_dictionaries(words):
    client = OpenAI()
    prompt = ('Écris moi les définitions adaptée pour des mots fléchés de la liste ci-dessous.'
            'Le format doit être uniquement un fichier json avec en clef le mot et en valeur la définition correspondante'
            'La longueur de chaque définition doit être inférieure à 20 caractères'
            f'Liste : "[\'{'\',\''.join(words)}\']"')
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    capelito_dictionary = json.loads(chat_completion.choices[0].message.content)
    return capelito_dictionary


def enrich_non_custom_capelitos(arrow_crossword: ArrowCrossword) -> ArrowCrossword:

    word_to_retrieve_capelito = [d.word for d in arrow_crossword.capelitos if not d.is_custom_capelito]
    capelito_dictionary = get_open_ai_dictionaries(word_to_retrieve_capelito)

    for d in arrow_crossword.capelitos:
        if d.word in capelito_dictionary:
            d.definition = capelito_dictionary[d.word]

    return arrow_crossword


