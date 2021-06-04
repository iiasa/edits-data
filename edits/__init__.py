from pathlib import Path
from typing import Collection, Dict, List

import yaml

from .format import Provider


def get_providers(ids: Collection[str] = None) -> List[Dict]:
    """Load information about the providers from :file:`providers.yaml`.

    If `ids` is provided, only entries with an ``id:`` field appearing in this list are
    returned. Otherwise, all entries are returned.
    """

    # Read the YAML file
    with open(Path(__file__).parents[1].joinpath("providers.yaml")) as f:
        raw = yaml.safe_load(f)

    # List of results
    result = []

    # Iterate over entries in the file
    for entry in raw:
        if ids and entry.get("id", None) not in ids:
            # This entry's ID is not one of the ones requested via the `ids` argument
            continue

        # Check that the entry is in a consistent format
        entry = Provider.check(entry)

        # Append to the results
        result.append(entry)

    # Return all the results
    return result
