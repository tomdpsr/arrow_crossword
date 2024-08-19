import datetime
import json

from shared_utilities.capelito.capelito import Capelito


def save_capelitos_to_json(
    capelitos: list[Capelito],
    score: int,
    map_file: str,
    capelito_file=None,
    mystery_capelito=None,
) -> dict:
    capelito_file = (
        capelito_file
        or f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{map_file}_{score}"
    )
    data_to_export = {
        "map_file": map_file,
        "score": score,
        "date": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "capelitos": [d.export_to_dict() for d in capelitos],
        "mystery_capelito": mystery_capelito,
    }
    with open(
        f"data/capelitos/{capelito_file}.json",
        "w",
    ) as f:
        json.dump(data_to_export, f)
    return data_to_export


def init_arrow_crossword_from_file(arrow_crossword_filename: str) -> list:
    f = open(f"data/capelitos/{arrow_crossword_filename}.json")
    arrow_crossword = json.load(f)
    arrow_crossword['capelitos'] = init_capelitos(arrow_crossword)
    return arrow_crossword


def init_capelitos(filled_map_json) -> list[Capelito]:
    all_capelitos = []
    for c in filled_map_json['capelitos']:
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
    return all_capelitos
