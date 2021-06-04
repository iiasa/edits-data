"""Fetch metadata over the Internet."""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import requests
import yaml


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
