import json

import pandas as pd
from openai import OpenAI

from arrow_crossword_generation.utilities.constants import (
    DICTIONARY_TO_PATH,
    DICTIONARY,
)
from shared_utilities.arrowed_place_holder.arrowed_place_holder import get_arrowed_place_holder
from shared_utilities.definition.definition import Definition


def enrich_custom_definitions(
    definitions: list[Definition],
    mystery_word: str
) -> tuple[list[Definition], int, str]:
    score = 0
    df_custom_dictionary = pd.read_csv(
        f"{DICTIONARY_TO_PATH[DICTIONARY.CUSTOM_DICTIONARY]}/{DICTIONARY.CUSTOM_DICTIONARY}.csv",
        dtype=object,
    )
    custom_definition_dictionary = dict(df_custom_dictionary.values)
    for d in definitions:
        custom_char = ''
        if d.word in custom_definition_dictionary:
            if not pd.isna(custom_definition_dictionary[d.word]):
                d.definition = custom_definition_dictionary[d.word] or d.definition
            d.is_custom_definition = True
            score += 1
            custom_char = '###'
        # PLACEHOLDER
        d.definition = d.word
        arrowed_place_holder = get_arrowed_place_holder(d.definition_type)
        print(f"{custom_char}({d.i},{d.j}, {arrowed_place_holder.unicode_char}) : {d.word}")

    # mystery word
    mystery_definition = mystery_word
    if not pd.isna(custom_definition_dictionary[mystery_word]):
        mystery_definition = custom_definition_dictionary[mystery_word] or mystery_definition
    return definitions, score, mystery_definition


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
    definition_dictionary = json.loads(chat_completion.choices[0].message.content)
    return definition_dictionary


def enrich_non_custom_definitions(definitions: list[Definition]) -> list[Definition]:
    word_to_retrieve_definition = [d.word for d in definitions if not d.is_custom_definition]
    definition_dictionary = get_open_ai_dictionaries(word_to_retrieve_definition)

    for d in definitions:
        if d.word in definition_dictionary:
            d.definition = definition_dictionary[d.word]

    return definitions


