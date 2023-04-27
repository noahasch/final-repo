"""Module to flag options."""
import click
from .works import Works


@click.command()
@click.argument("query", nargs=1)
@click.option("--bibtex", is_flag=True, show_default=True, default=False)
@click.option("--ris", is_flag=True, show_default=True, default=False)
def main(query, bibtex, ris):
    """Method to pass flags."""
    works = Works(query)
    if bibtex:
        print(works.bibtex)
    if ris:
        print(works.ris)
