# Demonstration of data descriptions

This repository provides a rudimentary example of decentralized metadata (descriptions of data), as a prototype for data exchange within the EDITS project.

## How to use

The code is written in Python.

1. Install the dependencies: `pip install -r requirements.txt`
2. In this directory, run the command-line tool with `python -m edits --help`.
   This shows the help information for the tool, e.g.:

   ```
   $ python -m edits --help
   Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

     Command-line interface for EDITS network metadata.

     See https://github.com/iiasa/edits-data for documentation.

   Options:
     --help  Show this message and exit.

   Commands:
     check  Check metadata formats for provider/file ID.
     demo   Demo code.
   ```

   Then give e.g. `python -m edits check --help` for help on specific commands.



The output of `edits demo` looks like:
```
Fetch data descriptions
Provider 1: 1 description(s)
Provider 2: 1 description(s)

Total 2 descriptions.

provider-1/dataset-X
  contains data classified as:
  ['Kind :: Survey', 'Availability :: Public']

provider-2/dataset-A
  contains data classified as:
  ['Kind :: Model output', 'Availability :: Collaborators only']
```

## How it works

- The file `providers.yaml` provides *registration*. It records, for each data provider, a location (a web URL) for data descriptions.
  - More data providers are ‘registered’ added by adding entries in this file.
  - For this demo, two other GitHub repositories are used:
    - https://github.com/khaeru/edits-data-demo-1
    - https://github.com/iiasa/edits-data-demo-2
- The code in `demo.py` ‘crawls’ or ‘scrapes’ these locations.
  From each location, it fetches a ZIP archive.
- Inside the archive are 1 or many files in a simple, text-based format.
- Each file contains a description of one “data set” (or related collection of data sets), structured with some mandatory and some optional fields.
- After having retrieved all the descriptions, ``demo.py`` can process it and generate outputs. In this example it:
  - Generates a unique ID like `provider-2/dataset-A` for each description.
  - Shows the “classifiers” for each one.

## Discussion

- This **software pattern** imitates more sophisticated standards such as SDMX, but aims to make the required technical capabilities for a data provider as low as possible.
  Precisely, these are:
  1. Edit text files (YAML template),
  2. Put 1 or more of these files in a ZIP archive, and
  3. Put that file on the Internet in a static location.

  These steps can all be done through basic GitHub features, but also using other tools.

- The pattern is **extensible** to, *inter alia*:
  - Output or write to a database or file(s) that can be used behind a user interface; in software like Excel, etc.
  - Retrieve descriptions stored in different places, such as:
    - Directories or collections of files rather than a ZIP archive.
    - File-sharing services such as Dropbox or Google Drive.
  - Provide feedback/pointers on broken URLs or malformed YAML files.

- The description **file format** can be specified by EDITS partners to:

  - Contain all information necessary to identify fruitful collaborations within EDITS.
  - Be re-usable and useful beyond the project.

  For instance, a provider could **re-use the same description** content/URL with 2 or more projects, or to advertise generally (outside any formal project) their model outputs or data offers.

- The pattern is **decentralized** and **asynchronous**.
  - Data providers can update their description(s) at any time by adding, modifying, or removing, YAML files to their collection.
  - The next run of `demo.py` (by whomever) will retrieve the latest descriptions.
  - Because `demo.py` and `providers.yaml` are public via this repository, anyone can access the full set of descriptions on demand, without any central coordination.

- The practice of creating and sharing these simple data descriptions through a simple process both (a) prepares the content and (b) develops fundamental skills for later using more sophisticated processes.
  The code can also be extended to support transforming the simple YAML descriptions into other metadata formats.
