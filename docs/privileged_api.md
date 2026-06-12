# Privileged API Reference

!!! warning
    Classes on this page target privileged endpoints and require valid `NMDCAuth` credentials.
    They are intended for authorized users who need metadata submission, identifier minting, or staging workflows.

## Authentication Support

`NMDCAuth` is required for all privileged classes on this page.

::: nmdc_client.auth.NMDCAuth

## Authentication Requirement

Instantiate `NMDCAuth` and pass it to privileged classes:

```python
from nmdc_client.auth import NMDCAuth
from nmdc_client.metadata import Metadata

auth = NMDCAuth(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")
metadata_client = Metadata(auth=auth)
```

## Metadata Submission

::: nmdc_client.metadata.Metadata

## Identifier Minting

::: nmdc_client.minter.Minter

## Data Staging and Workflow Management

::: nmdc_client.data_staging.JGISequencingProjectAPI

::: nmdc_client.data_staging.JGISampleSearchAPI

::: nmdc_client.data_staging.GlobusTaskAPI

## Related Pages

- [Core Search API Reference](functions.md) for public core APIs
- [`CollectionSearch` Subclasses](public_subclasses.md) for public collection subclasses
