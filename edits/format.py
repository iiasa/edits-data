"""Formats for YAML and other files."""

from typing import Dict


class Provider:
    @staticmethod
    def check(info: Dict) -> Dict:
        """Check `info` about a data provider e.g. from :file:`providers.yaml`.

        Raises AssertionError if the data is not in a correct format.
        """

        # Required keys
        for key in ("id", "contact", "files"):
            if key not in info:
                print(f"Provider entry missing {repr(key)} key: {info}")
                assert False

        # file: key must be a list of strings
        if not isinstance(info["files"], list) or not all(
            isinstance(f, str) for f in info["files"]
        ):
            print(
                f"Provider '{info['id']}' 'files' key is not a list of strings: "
                + repr(info["files"])
            )
            assert False

        return info

    @staticmethod
    def print(entry):
        """Display a provider `entry`."""

        print(f"\nProvider: {id}")
        print(f"Contact: {entry['contact']['name']} <{entry['contact']['email']}>")

        print(f"\n{len(entry['files'])} file(s):")
        print("\n".join(entry["files"]))
        print()
