import json

from openai import OpenAI

from arrow_crossword_graphical_interface.generate_graphic_crossword import init_definitions
from shared_utilities.definition.utilities import save_definitions_to_json


def get_open_ai_dictionnaries(words, client):
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

def enrich_arrow_crossword_definition(definitions: str):
    client = OpenAI()
    f = open(f"data/definitions/{definitions}.json")
    filled_map_json = json.load(f)
    all_definitions = init_definitions(filled_map_json)
    word_to_retrieve_definition = [d.word for d in all_definitions if not d.is_custom_definition]
    definition_dictionary = get_open_ai_dictionnaries(word_to_retrieve_definition, client)
    for d in all_definitions:
        if d.word in definition_dictionary:
            d.definition = definition_dictionary[d.word]
    save_definitions_to_json(
        definitions=all_definitions,
        score=filled_map_json["score"],
        map_file=filled_map_json["map_file"],
        deifinition_file=definitions,
    )




