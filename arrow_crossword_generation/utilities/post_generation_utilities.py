import json

import pandas as pd
from loguru import logger
from openai import OpenAI

from arrow_crossword_generation.utilities.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
)
from shared_utilities.arrowed_place_holder.arrowed_place_holder import get_arrowed_place_holder
from shared_utilities.capelito.capelito import Capelito


def enrich_custom_capelitos(
    capelitos: list[Capelito],
    mystery_capelito_word: str
) -> tuple[list[Capelito], int, str]:
    score = 0
    df_custom_dictionary = pd.read_csv(
        f"{DICTIONARY_TO_PATH[DICTIONARY.CUSTOM_DICTIONARY]}/{DICTIONARY.CUSTOM_DICTIONARY}.csv",
        dtype=object,
    )
    custom_capelito_dictionary = dict(df_custom_dictionary.values)
    for d in capelitos:
        custom_char = ''
        if d.word in custom_capelito_dictionary:
            if not pd.isna(custom_capelito_dictionary[d.word]):
                d.capelito = custom_capelito_dictionary[d.word] or d.capelito
            d.is_custom_capelito = True
            score += 1
            custom_char = '###'
        # PLACEHOLDER
        d.capelito = d.word
        arrowed_place_holder = get_arrowed_place_holder(d.capelito_type)
        logger.info(f"{custom_char}({d.i},{d.j}, {arrowed_place_holder.unicode_char}) : {d.word}")

    # mystery word
    mystery_capelito_definition = None
    if mystery_capelito_word:
        if not pd.isna(custom_capelito_dictionary[mystery_capelito_word]):
            mystery_capelito_definition = custom_capelito_dictionary[mystery_capelito_word] or mystery_capelito_word
    return capelitos, score, mystery_capelito_definition


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


def enrich_non_custom_capelitos(capelitos: list[Capelito]) -> list[Capelito]:
    word_to_retrieve_capelito = [d.word for d in capelitos if not d.is_custom_capelito]
    capelito_dictionary = get_open_ai_dictionaries(word_to_retrieve_capelito)

    for d in capelitos:
        if d.word in capelito_dictionary:
            d.capelito = capelito_dictionary[d.word]

    return capelitos


