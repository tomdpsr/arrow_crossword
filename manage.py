import click

from create_dictionnary import create_dictionnary
from generate_arrow_crossword import generate_arrow_crossword
from generate_graphic_crossword import generate_graphic_crossword


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-d", "--dict-folder", show_default=True, default="usito", help="help"
)
@click.option("-m", "--map-file", show_default=True, default="map_1", help="help")
def generate_arrow_crosswords(dict_folder, map_file):
    for i in range(20):
        generate_arrow_crossword(dict_folder, map_file)


@cli.command()
@click.option("-d", "--dict-folder", show_default=True, default="perso", help="help")
def create_dictionnaries(dict_folder):
    create_dictionnary(dict_folder)


@cli.command()
@click.option(
    "-f", "--filled-map", show_default=True, default="20240625125906_8", help="help"
)
def generate_graphic_crosswords(filled_map):
    generate_graphic_crossword(filled_map)


if __name__ == "__main__":
    cli()
