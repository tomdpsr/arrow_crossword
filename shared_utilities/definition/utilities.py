import datetime
import json

from shared_utilities.definition.definition import Definition


def save_definitions_to_json(
    definitions: list[Definition],
    score: int,
    map_file: str,
    definition_file=None,
    mystery_word=None,
) -> None:
    definition_file = (
        definition_file
        or f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{map_file}_{score}"
    )
    data_to_export = {
        "map_file": map_file,
        "score": score,
        "date": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "definitions": [d.export_to_dict() for d in definitions],
        "mystery_word": mystery_word,
    }
    with open(
        f"data/validated_definitions/{definition_file}.json",
        "w",
    ) as f:
        json.dump(data_to_export, f)


def init_definitions(filled_map_json) -> list[Definition]:
    all_definitions = []
    for d in filled_map_json["definitions"]:
        dd = Definition(
            definition_type=d["definition_type"],
            i=d["i"],
            j=d["j"],
            word=d["word"],
            definition=d["definition"],
            is_custom_definition=d["is_custom_definition"],
        )
        all_definitions.append(dd)

    # Sorry for the n square
    for d in all_definitions:
        if d.linked_definition is None:
            for d2 in all_definitions:
                if d.i == d2.i and d.j == d2.j and d.word != d2.word:
                    d.linked_definition, d2.linked_definition = d2, d
    return all_definitions
