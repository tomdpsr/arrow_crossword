import pytest
from back.arrow_crossword_generation.generate_arrow_crossword import (
    generate_arrow_crossword,
)
from back.shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword


def test_generate_arrow_crossword_basic(test_data_dir, test_env, mock_dictionary_paths):
    map_file = f"test_map"
    result = generate_arrow_crossword("main_dictionary", str(map_file))
    assert isinstance(result, ArrowCrossword)
    assert len(result.capelitos) > 0


def test_backtracking_success(test_data_dir, test_env, dictionary_handler):
    arrow_crossword = ArrowCrossword(str(test_data_dir / "test_map.csv"))
    opts = {"nb_max_tries_per_word": 10, "nb_custom_capelitos_min": 1}
    validated_custom_words = []
    arrow_crossword.init_state(dictionary_handler, validated_custom_words, opts)

    assert len(arrow_crossword.capelitos) > 0
    for capelito in arrow_crossword.capelitos:
        assert hasattr(capelito, "word")
        assert hasattr(capelito, "is_set")


def test_dictionary_loading(dictionary_handler):
    assert 2 in dictionary_handler.main_words
    assert 3 in dictionary_handler.main_words
    assert len(dictionary_handler.main_words[2]) > 0
    assert len(dictionary_handler.main_words[3]) > 0


@pytest.mark.parametrize(
    "invalid_input",
    [
        ("nonexistent_folder", "map.csv"),
        ("tests/data", "nonexistent_map.csv"),
    ],
)
def test_generate_arrow_crossword_invalid_input(invalid_input, test_env):
    with pytest.raises(Exception):
        generate_arrow_crossword(*invalid_input)
