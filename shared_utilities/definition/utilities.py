import datetime
import json

from shared_utilities.definition.definition import Definition


def save_definitions_to_json(
    definitions: list[Definition], score: int, map_file: str, deifinition_file=None
) -> None:
    deifinition_file = (
        deifinition_file
        or f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{score}"
    )
    data_to_export = {
        "map_file": map_file,
        "score": score,
        "date": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "definitions": [d.export_to_dict() for d in definitions],
    }
    with open(
        f"data/definitions/{deifinition_file}.json",
        "w",
    ) as f:
        json.dump(data_to_export, f)
