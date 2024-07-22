from collections import namedtuple

ArrowedPlaceHolder = namedtuple(
    "ArrowedPlaceHolder",
    [
        "capelito_type",
        "i_diff",
        "j_diff",
        "is_horizontal",
        "unicode_char",
        "upper_location",
    ],
)

ArrowedPlaceHolders = [
    ArrowedPlaceHolder(
        capelito_type="1",
        i_diff=0,
        j_diff=1,
        is_horizontal=True,
        unicode_char="\u2192",
        upper_location=True,
    ),
    ArrowedPlaceHolder(
        capelito_type="2",
        i_diff=1,
        j_diff=0,
        is_horizontal=False,
        unicode_char="\u2193",
        upper_location=False,
    ),
    ArrowedPlaceHolder(
        capelito_type="3",
        i_diff=0,
        j_diff=1,
        is_horizontal=False,
        unicode_char="\u21B4",
        upper_location=True,
    ),
    ArrowedPlaceHolder(
        capelito_type="4",
        i_diff=0,
        j_diff=-1,
        is_horizontal=False,
        unicode_char="\u21B4",
        upper_location=True,
    ),
    ArrowedPlaceHolder(
        capelito_type="5",
        i_diff=-1,
        j_diff=0,
        is_horizontal=True,
        unicode_char="\u21B1",
        upper_location=False,
    ),
    ArrowedPlaceHolder(
        capelito_type="6",
        i_diff=1,
        j_diff=0,
        is_horizontal=True,
        unicode_char="\u21B3",
        upper_location=False,
    ),
]


def get_arrowed_place_holder(capelito_type: str) -> ArrowedPlaceHolder:
    return next(
        x
        for x in ArrowedPlaceHolders
        if getattr(x, "capelito_type") == capelito_type
    )
