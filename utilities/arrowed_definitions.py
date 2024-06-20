from collections import namedtuple
from dataclasses import dataclass

ArrowedDefinition = namedtuple(
    "ArrowedDefinition",
    [
        "definition_type",
        "i_diff",
        "j_diff",
        "is_horizontal",
        "unicode_char",
        "text_diff",
    ],
)

TEXT_DIFF_BASE = 7

ArrowedDefinitions = [
    ArrowedDefinition(
        definition_type="1",
        i_diff=0,
        j_diff=1,
        is_horizontal=True,
        unicode_char="\u2192",
        text_diff=-TEXT_DIFF_BASE,
    ),
    ArrowedDefinition(
        definition_type="2",
        i_diff=1,
        j_diff=0,
        is_horizontal=False,
        unicode_char="\u2193",
        text_diff=TEXT_DIFF_BASE,
    ),
    ArrowedDefinition(
        definition_type="3",
        i_diff=0,
        j_diff=1,
        is_horizontal=False,
        unicode_char="\u21B4",
        text_diff=-TEXT_DIFF_BASE,
    ),
    ArrowedDefinition(
        definition_type="4",
        i_diff=0,
        j_diff=-1,
        is_horizontal=False,
        unicode_char="\u21B4",
        text_diff=TEXT_DIFF_BASE,
    ),
    ArrowedDefinition(
        definition_type="5",
        i_diff=-1,
        j_diff=0,
        is_horizontal=True,
        unicode_char="\u21B1",
        text_diff=TEXT_DIFF_BASE,
    ),
    ArrowedDefinition(
        definition_type="6",
        i_diff=1,
        j_diff=0,
        is_horizontal=True,
        unicode_char="\u21B3",
        text_diff=TEXT_DIFF_BASE,
    ),
]


def get_arrowed_definitions(definition_type: str) -> ArrowedDefinition:
    return next(
        x
        for x in ArrowedDefinitions
        if getattr(x, "definition_type") == definition_type
    )


def get_arrowed_definition_mapping(attribute):
    return {
        getattr(ad, "definition_type"): getattr(ad, attribute)
        for ad in ArrowedDefinitions
    }
