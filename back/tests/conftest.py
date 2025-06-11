import os
import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def env_test():
    os.environ["NB_MAX_TRIES_PER_WORD"] = "10"
    os.environ["NB_CUSTOM_CAPELITOS_MIN"] = "0"


@pytest.fixture()
def mock_dictionary_paths(monkeypatch, request):
    print(request.param)
    test_param = request.param
    test_data_dir = Path(__file__).parent / "data" / test_param
    mock_paths = {
        "custom_dictionary": test_data_dir,
        "forbidden_dictionary": test_data_dir,
        "main_dictionary": test_data_dir,
    }
    monkeypatch.setattr(
        "back.shared_utilities.dictionary_handler.constants.DICTIONARY_TO_PATH",
        mock_paths,
    )
    monkeypatch.setattr(
        "shared_utilities.arrow_crossword.arrow_crossword.RESOURCES_FOLDER", f"data/{test_param}"
    )



@pytest.fixture()
def mock_dictionary_handler(mock_dictionary_paths):
    from back.shared_utilities.dictionary_handler.dictionary_handler import (
        DictionaryHandler,
    )

    return DictionaryHandler("main_dictionary")
