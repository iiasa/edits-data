"""Command-line interface for EDITS network metadata.

See https://github.com/iiasa/edits-data for documentation.
"""
import click
import subprocess
import yaml
from pathlib import Path

from . import get_providers
from .remote import fetch_all, fetch_single


@click.group(help=__doc__)
def cli():
    # Show the current git version
    try:
        version = (
            subprocess.check_output(["git", "log", "-1", "--format=reference"])
            .decode()
            .split()[0],
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        version = "(unknown)"

    print(f"EDITS version: {version}\n")


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
            desc = fetch_single(file, provider=entry)
        except Exception as e:
            print(repr(e))
        else:
            print(*[repr(d) for d in desc], sep="\n")

    print("--- done.")


@cli.command()
@click.argument("expression")
def search(expression):
    """Search for matching metadata.

    EXPRESSION must be of the form KIND=KEY. KIND must be either "dimension" or
    "measure"; KEY is a string or fragment that must occur in the ID. For example:

    python -m edits search dimension=foo

    …will show every dimension named "foo", but also "food" or "other_foo" etc., across
    all data providers.
    """
    # Split the expression into `kind` and `key`
    kind, key = expression.split("=")

    # Check for the kinds of search currently supported
    if kind not in {"dimension", "measure"}:
        raise click.ClickException(f"Can't search for {repr(kind)}")

    # True if there is at least 1 match
    matched = False

    # Loop over all descriptions
    for d in fetch_all():
        # Loop over dimensions (or measures) in this description
        for id, info in getattr(d, kind).items():
            if key in id:
                # `key` appears in `id` → this is a match
                matched = True

                # Print the matching entry
                print(
                    f"--- {d.full_id}",
                    yaml.dump({id: info}).replace("\n\n", "\n"),
                    "",
                    sep="\n",
                )

    if not matched:
        print("No matches")


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
