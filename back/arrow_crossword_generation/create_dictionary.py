from pathlib import Path

import pandas as pd
import unidecode

from back.shared_utilities.dictionary_handler.constants import DICTIONARY_TO_PATH


def clean_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    df["word"] = df["word"].astype(str).replace("[^a-zA-Z]", "")
    df["word"] = df["word"].apply(
        lambda x: unidecode.unidecode(x.lower().replace("-", ""))
    )
    df["word"] = df["word"].str.replace("[^a-zA-Z]", "", regex=True)
    df = df.drop_duplicates()
    return df


def create_dictionary(dictionary: str):
    df = pd.read_csv(f"{DICTIONARY_TO_PATH[dictionary]}/{dictionary}.csv", dtype=object)

    df = clean_dictionary(df)

    for i in range(2, 26):
        df_i = df[df["word"].str.len() == i]
        df_i["word"] = df_i["word"].str.lower()
        Path(f"{DICTIONARY_TO_PATH[dictionary]}/{dictionary}").mkdir(
            parents=True, exist_ok=True
        )
        df_i["word"].to_csv(
            f"{DICTIONARY_TO_PATH[dictionary]}/{dictionary}/word_{i}.csv",
            sep=",",
            index=False,
            header=False,
        )
