from collections import namedtuple
from dataclasses import dataclass

ArrowedDefinition = namedtuple('ArrowedDefinition', ['definition_type', 'i_diff', 'j_diff', 'is_horizontal'])

ArrowedDefinitions = [
    ArrowedDefinition(definition_type='1', i_diff=0, j_diff=1, is_horizontal=True),
    ArrowedDefinition(definition_type='2', i_diff=1, j_diff=0, is_horizontal=False),
    ArrowedDefinition(definition_type='3', i_diff=0, j_diff=1, is_horizontal=False),
    ArrowedDefinition(definition_type='4', i_diff=0, j_diff=-1, is_horizontal=False),
    ArrowedDefinition(definition_type='5', i_diff=-1, j_diff=0, is_horizontal=True),
    ArrowedDefinition(definition_type='6', i_diff=1, j_diff=0, is_horizontal=True),
]

def get_arrowed_definition_mapping(attribute):
    return {getattr(ad, 'definition_type'): getattr(ad, attribute) for ad in ArrowedDefinitions}

