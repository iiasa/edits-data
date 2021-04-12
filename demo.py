from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import click
import requests
import yaml


@click.command()
def cli():
    """Command-line interface for accessing the data."""

    # Load information about the providers from file
    with open("providers.yaml") as f:
        providers = yaml.safe_load(f)

    # List of individual data descriptions
    all_descriptions = []

    # Fetch data descriptions from each provider
    print("Fetch data descriptions")

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


def get_descriptions(info):
    """Return a set of data descriptions based on `info`."""

    # List to collect the individual data descriptions
    results = []

    # Retrieve the URL given in providers.yaml, over the Internet
    response = requests.get(info["url"])

    # Open the ZIP archive
    with ZipFile(BytesIO(response.content)) as zf:

        # Loop over each file in the ZIP archive
        for file_info in zf.infolist():

            # Check the file name
            if not file_info.filename.endswith(".yaml"):
                # Not a data description file; ignore
                continue

            # Load the description from the file in the ZIP archive
            desc = yaml.safe_load(zf.open(file_info.filename))

            # Store a unique ID for this datadescription
            desc["id"] = (
                info["name"].lower().replace(" ", "-")
                + "/"
                + Path(file_info.filename).stem
            )

            # Store the description
            results.append(desc)

    # Return all descriptions
    return results


if __name__ == "__main__":
    # Start the command-line interface
    cli()
