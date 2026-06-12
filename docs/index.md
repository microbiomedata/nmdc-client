# NMDC Client Documentation

NMDC Client is a Python package for interacting with selected endpoints of the [NMDC Runtime API](https://api.microbiomedata.org/docs).
It supports querying public NMDC metadata and, for authorized users, working with privileged submission and staging endpoints.

NMDC Client is published on PyPI as `nmdc-client` and imported in Python as `nmdc_client`.

## Getting Started

- [Quick Start](usage.ipynb) — class selection and workflow guidance
- [Using MongoDB Filters](filters.ipynb) — Python filter recipes and troubleshooting
- [External Notebook Examples](example_usage.md) — end-to-end notebook exemplars

## API Reference

Public and privileged APIs are documented separately. Most will want to start with public search classes.
Privileged API classes are for users with submission and staging permissions and are not needed for general querying of public metadata.

- [Core Search API Reference](functions.md) — public, reusable core classes
- [`CollectionSearch` Subclasses](public_subclasses.md) — collection-specific search classes
- [Privileged API Reference](privileged_api.md) — auth, metadata submission, minting, and staging
