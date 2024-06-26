import datetime
import json

from utilities.definition.definition import Definition


def save_definitions_to_json(
    definitions: list[Definition], score: int, map_file: str, filled_map_file=None
) -> None:
    filled_map_file = (
        filled_map_file or f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{score}"
    )
    data_to_export = {
        "map_file": map_file,
        "score": score,
        "date": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "definitions": [d.export_to_dict() for d in definitions],
    }
    with open(
        f"resources/filled_maps/{filled_map_file}.json",
        "w",
    ) as f:
        json.dump(data_to_export, f)
