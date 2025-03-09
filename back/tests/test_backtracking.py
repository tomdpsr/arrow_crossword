import os
import pytest
from pathlib import Path


@pytest.fixture
def mock_resources_path(monkeypatch):
    monkeypatch.setattr(
        "shared_utilities.arrow_crossword.arrow_crossword.RESOURCES_FOLDER", "data"
    )


def test_backtracking(mock_dictionary_handler, mock_resources_path, monkeypatch):
    from shared_utilities.arrow_crossword.arrow_crossword import ArrowCrossword
    from arrow_crossword_generation.generate_arrow_crossword import backtracking
    from arrow_crossword_generation.utilities.generation_utilities import (
        check_number_capelito_is_set,
    )

    opts = {
        "nb_max_tries_per_word": 100,
        "nb_custom_capelitos_min": 2,
    }

    def mock_shuffle_and_tag_capelitos(self, opts):
        custom_capelitos = [
            next(
                c
                for c in self.capelitos
                if c.i == 8 and c.j == 0 and c.capelito_type == "1"
            ),
            next(
                c
                for c in self.capelitos
                if c.i == 2 and c.j == 0 and c.capelito_type == "1"
            ),
        ]
        for capelito in custom_capelitos:
            capelito.is_custom_capelito = True
        remaining_capelitos = [c for c in self.capelitos if c not in custom_capelitos]

        return custom_capelitos + remaining_capelitos

    monkeypatch.setattr(
        "shared_utilities.arrow_crossword.arrow_crossword.ArrowCrossword.shuffle_and_tag_capelitos",
        mock_shuffle_and_tag_capelitos,
    )

    arrow_crossword = ArrowCrossword(map_file="map_s")
    arrow_crossword.init_state(mock_dictionary_handler, [], opts)

    backtracking(
        0,
        arrow_crossword,
        mock_dictionary_handler,
        opts,
        max_size=len(arrow_crossword.capelitos),
    )

    # Assertions to verify the expected behavior
    assert (
        check_number_capelito_is_set(
            arrow_crossword.capelitos, len(arrow_crossword.capelitos)
        )
        is True
    )
