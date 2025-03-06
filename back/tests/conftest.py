import os
import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir():
    return Path(__file__).parent / "data"


@pytest.fixture
def test_env():
    os.environ["NB_MAX_TRIES_PER_WORD"] = "10"
    os.environ["NB_CUSTOM_CAPELITOS_MIN"] = "1"


@pytest.fixture
def dictionary_handler(test_data_dir):
    from back.shared_utilities.dictionary_handler.dictionary_handler import (
        DictionaryHandler,
    )

    return DictionaryHandler(str(test_data_dir))


@pytest.fixture(autouse=True)
def mock_dictionary_paths(monkeypatch, test_data_dir):
    mock_paths = {
        "custom_dictionary": f"{test_data_dir}/custom_dictionary",
        "forbidden_dictionary": f"{test_data_dir}/custom_dictionary",
        "main_dictionary": f"{test_data_dir}/custom_dictionary",
    }
    monkeypatch.setattr(
        "back.shared_utilities.dictionary_handler.constants.DICTIONARY_TO_PATH",
        mock_paths,
    )
    # monkeypatch.setattr("back.shared_utilities.constants.DICTIONARY_TO_PATH", mock_paths)
    # monkeypatch.setattr("shared_utilities.constants.DICTIONARY_TO_PATH", mock_paths)
    # monkeypatch.setattr("back.dictionary_handler.constants.DICTIONARY_TO_PATH", mock_paths)
    return mock_paths
