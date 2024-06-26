import click

from arrow_crossword_generation.create_dictionnary import create_dictionary
from arrow_crossword_generation.enrich_arrow_crossword_definition import (
    enrich_arrow_crossword_definition,
)
from arrow_crossword_generation.generate_arrow_crossword import generate_arrow_crossword
from arrow_crossword_generation.utilities.constants import DICTIONARY
from arrow_crossword_graphical_interface.generate_graphic_crossword import (
    generate_graphic_crossword,
)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-d",
    "--dict-folder",
    show_default=True,
    default=DICTIONARY.FRENCH_DICTIONARY,
    help="help",
)
def create_dictionaries(dict_folder):
    create_dictionary(dict_folder)


@cli.command()
@click.option(
    "-d",
    "--dictionary",
    show_default=True,
    default=DICTIONARY.FRENCH_DICTIONARY,
    help="help",
)
@click.option("-m", "--map-file", show_default=True, default="map_1", help="help")
def generate_arrow_crosswords(dictionary, map_file):
    generate_arrow_crossword(dictionary, map_file)


@cli.command()
@click.option(
    "-d", "--definitions", show_default=True, default="20240626211422_3", help="help"
)
def enrich_arrow_crossword_definitions(definitions):
    enrich_arrow_crossword_definition(definitions)


@cli.command()
@click.option(
    "-d", "--definitions", show_default=True, default="20240626211422_3", help="help"
)
def generate_graphic_crosswords(definitions):
    generate_graphic_crossword(definitions)


if __name__ == "__main__":
    cli()
