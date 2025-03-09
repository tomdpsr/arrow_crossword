import os
import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def test_data_dir():
    return Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def test_env():
    os.environ["NB_MAX_TRIES_PER_WORD"] = "10"
    os.environ["NB_CUSTOM_CAPELITOS_MIN"] = "1"


@pytest.fixture(autouse=True)
def mock_dictionary_paths(monkeypatch, test_data_dir):
    mock_paths = {
        "custom_dictionary": test_data_dir,
        "forbidden_dictionary": test_data_dir,
        "main_dictionary": test_data_dir,
    }
    monkeypatch.setattr(
        "back.shared_utilities.dictionary_handler.constants.DICTIONARY_TO_PATH",
        mock_paths,
    )


@pytest.fixture()
def mock_dictionary_handler(monkeypatch, test_data_dir):
    from back.shared_utilities.dictionary_handler.dictionary_handler import (
        DictionaryHandler,
    )

    return DictionaryHandler("main_dictionary")
