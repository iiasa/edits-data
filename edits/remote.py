"""Fetch metadata over the Internet."""
from io import BytesIO
from itertools import chain
from pathlib import Path
from typing import List
from urllib.parse import urlparse
from zipfile import ZipFile

import requests
import yaml

from . import get_providers
from .format import Description, Provider


def fetch_all(provider=None) -> List[Description]:
    """Fetch all data descriptions for a given `provider`.

    If no `provider` is given, fetch all descriptions for all providers.
    """
    providers = [provider] if provider else get_providers()

    iters = []
    for p in providers:
        iters.extend(fetch_single(url, p) for url in p.files)

    return list(chain(*iters))


def fetch_single(url: str, provider: Provider) -> List[Description]:
    """Retrieve the data from `url`.

    `provider` is used to construct data set IDs.
    """
    response = requests.get(url)

    if url.endswith(".yaml"):
        id = Path(urlparse(url).path).stem
        try:
            return [
                Description.from_file(response.content, id=id, provider_id=provider.id)
            ]
        except Exception as e:
            # Something wrong with the formatting
            print(f"{repr(e)} when loading:\n  {url}")
            if isinstance(e, yaml.scanner.ScannerError):
                mark = e.args[-1]
                print(f"At line {mark.line}, column {mark.column}")
            return []
    elif url.endswith("zip"):
        return from_zip(BytesIO(response.content))


def from_zip(file, name):
    """Collect descriptions from a ZIP archive."""

    # List to collect the individual data descriptions
    results = []

    # Open the ZIP archive
    with ZipFile(file) as zf:

        # Loop over each file in the ZIP archive
        for file_info in zf.infolist():

            # Check the file name
            if not file_info.filename.endswith(".yaml"):
                # Not a data description file; ignore
                continue

            # Load the description from the file in the ZIP archive
            try:
                desc = Description.from_file(
                    zf.open(file_info.filename), id=Path(file_info.filename).stem
                )
            except Exception as e:
                # Something wrong with the formatting
                print(
                    f"{repr(e)} when loading:\n  {repr(file_info.filename)}\n"
                    "…skipping.\n"
                )
                continue

            # Store a unique ID for this datadescription
            desc.id = (
                name.lower().replace(" ", "-") + "/" + Path(file_info.filename).stem
            )

            # Store the description
            results.append(desc)

    # Return all descriptions
    return results
