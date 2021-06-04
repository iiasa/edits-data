"""Command-line interface for EDITS network metadata."""
import click
import subprocess
from pathlib import Path

from . import get_providers
from .remote import fetch_all, fetch_single


@click.group()
def cli():
    """EDITS network metadata."""
    # Show the current git version
    print(
        "EDITS version:",
        subprocess.check_output(["git", "log", "-1", "--format=reference"]).decode(),
    )


@cli.command()
@click.option("--local", is_flag=True, help="ID is a local YAML file.")
@click.argument("id")
def check(local, id):
    """Check metadata formats for provider/file ID.

    If --local is given, the ID is just the path to a local file, which is checked
    directly. Otherwise, the contents of providers.yaml are checked, and then used to
    retrieve 0 or more files over the internet. Those files are then checked one at a
    time.
    """

    if local:
        files = [Path(id)]
    else:
        print(
            f"Check metadata formats for provider: {id}\n\n"
            "--- Information in providers.yaml"
        )

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
        files = entry.files

        # Display information about the entry
        print(repr(entry))

    print("\n--- Data description files")

    for file in files:
        print(f"--- {file}")

        try:
            desc = fetch_single(file)
        except Exception as e:
            print(repr(e))
        else:
            print(*[repr(d) for d in desc], sep="\n")

    print("--- done.")


@cli.command()
def demo():
    """Demo code."""
    # List of individual data descriptions
    all_descriptions = []

    # Fetch data descriptions from each provider
    print("Fetch data descriptions")

    providers = get_providers()
    for provider in providers:

        print(f"{provider}:")

        descriptions = fetch_all(provider)

        # Show some description of what was fetched
        print(f"…retrieved {len(descriptions)} description(s).\n")

        # Add to the list
        all_descriptions.extend(descriptions)

    # Finished retrieving

    # Summary information
    print(f"\nTotal {len(all_descriptions)} descriptions.\n")

    # Example of processing the descriptions: show the classifiers
    for desc in all_descriptions:
        print(
            f"{desc}",
            "contains data classified as:",
            "  " + repr(desc.classifiers),
            sep="\n",
            end="\n\n",
        )


# Invoke the CLI
cli()
