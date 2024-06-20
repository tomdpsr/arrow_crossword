from pathlib import Path

import pandas as pd
import unidecode

from utilities.garbage import letter_to_score


def create_dictionnary(dict_folder: str):
    print(1)
    df = pd.read_csv(
        f"resources/dicts/base_files/mots_{dict_folder}.csv", header=None, dtype=object
    )
    df[0] = df[0].astype(str).replace("[^a-zA-Z]", "")
    df[0] = df[0].apply(lambda x: unidecode.unidecode(x.lower().replace("-", "")))
    df[0] = df[0].str.replace("[^a-zA-Z]", "", regex=True)
    df = df.drop_duplicates()

    for i in range(2, 26):
        df_i = df[df[0].str.len() == i]
        df_i[0] = df_i[0].str.lower()
        df_i["score"] = df_i[0].apply(
            lambda x: sum([letter_to_score[character.upper()] for character in x])
        )
        df_i = df_i.sort_values(by="score", ascending=True)
        Path(f"resources/dicts/{dict_folder}").mkdir(parents=True, exist_ok=True)
        df_i[0].to_csv(
            f"resources/dicts/{dict_folder}/mots_{i}.csv",
            sep=",",
            index=False,
            header=False,
        )
