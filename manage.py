import click

from create_dictionnary import create_dictionnary
from generate_arrow_crossword import generate_arrow_crossword


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--dict-folder', show_default=True, default='full_dict', help='help')
@click.option('-m', '--map-file', show_default=True, default='map_super_mall', help='help')
def generate_arrow_crosswords(dict_folder, map_file):
    generate_arrow_crossword(dict_folder, map_file)


@cli.command()
@click.option('-d', '--dict-folder', show_default=True, default='perso', help='help')
def create_dictionnaries(dict_folder):
    create_dictionnary(dict_folder)


if __name__ == '__main__':
    cli()
