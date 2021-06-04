"""Command-line interface for EDITS network metadata."""
import click

from . import get_providers
from .format import Provider
from .remote import get_descriptions


@click.group()
def cli():
    """EDITS network metadata."""


@cli.command()
@click.argument("id")
def check(id):
    """Check metadata formats for provider ID."""
    # Load the provider information matching `id`
    entries = get_providers([id])

    # Check for 0 or 2 or more entries
    if len(entries) == 0:
        raise click.ClickException(f"No provider.yaml entry with id: {id}")
    elif len(entries) > 1:
        raise click.ClickException(
            f"Duplicate provider.yaml entries with id: {id}\n"
            "Each ID should be used only once."
        )

    # Keep the single entry
    entry = entries[0]

    # Display information about the entry
    Provider.print(entry)


@cli.command()
def demo():
    # List of individual data descriptions
    all_descriptions = []

    # Fetch data descriptions from each provider
    print("Fetch data descriptions")

    providers = get_providers()
    for provider in providers:

        descriptions = get_descriptions(provider)

        # Show some description of what was fetched
        print(f"{provider['name']}: {len(descriptions)} description(s)")

        # Add to the list
        all_descriptions.extend(descriptions)

    # Finished retrieving

    # Summary information
    print(f"\nTotal {len(all_descriptions)} descriptions.\n")

    # Example of processing the descriptions: show the classifiers
    for desc in all_descriptions:
        print(
            f"{desc['id']}",
            "contains data classified as:",
            repr(desc["classifiers"]),
            sep="\n  ",
            end="\n\n",
        )


# Invoke the CLI
cli()
