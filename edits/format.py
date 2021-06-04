"""Formats for YAML and other files."""
import logging

import yaml
from sdmx.model import Concept, PrimaryMeasure

log = logging.getLogger(__name__)


class Provider:
    """Check `info` about a data provider e.g. from :file:`providers.yaml`.

    Raises AssertionError if the data is not in a correct format.
    """

    def __init__(self, info):
        # Required fields
        for field in ("id", "contact", "files"):
            if field not in info:
                raise ValueError(f"Provider entry missing {repr(field)} key: {info}")

            setattr(self, field, info[field])

        # file: key must be a list of strings
        if not isinstance(self.files, list) or not all(
            isinstance(f, str) for f in self.files
        ):
            raise TypeError(
                "Provider '{0.id}' 'files:' is not a list of strings: {0.files}".format(
                    self
                )
            )

    def __str__(self):
        """Short string representation."""
        return f"Provider: {self.id}"

    def __repr__(self):
        """Long string representation."""
        return f"""{self}
Contact: {self.contact['name']} <{self.contact['email']}>

{len(self.files)} file(s):
""" + "\n".join(
            self.files
        )


class Description:
    """Class corresponding to a data description file."""

    def __init__(self, info):
        self.id = info.pop("id", "foo")

        self.provider_id = info.pop("provider_id", None)
        self.provider = info.pop("provider", dict())
        if len(self.provider) == 0:
            print("provider: section is missing or empty")

        self.title = info.pop("title")
        self.description = info.pop("description")

        self.classifiers = info.get("classifiers", [])
        if len(self.classifiers) == 0:
            print("classifiers: section is missing or empty")

        if "measures" in info:
            log.debug("measures: section renamed measure:")
            info["measure"] = info.pop("measures")

        self.measure = info.pop("measure")

        if "dimensions" in info:
            log.debug("dimensions: section renamed dimension:")
            info["dimension"] = info.pop("dimensions")

        self.dimension = info.pop("dimension")

        if "data" in info:
            log.debug("data: section renamed quantity:")
            info["quantity"] = info.pop("data")

        self.quantity = info.pop("quantity")

    @classmethod
    def from_file(cls, content, **kwargs):
        kwargs.update(yaml.safe_load(content))
        return cls(kwargs)

    @property
    def full_id(self):
        return f"{self.provider_id}/{self.id}"

    def __repr__(self):
        return f"""Description {self.full_id}: {self.title}

{self.description}

Classifiers: {self.classifiers}

{len(self.measure)} measure(s)
{len(self.dimension)} dimension(s)
{len(self.quantity)} quantities
"""
