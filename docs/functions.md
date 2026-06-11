# Core Search API Reference

This page documents public, reusable core classes.
Collection-specific subclasses are documented in [`CollectionSearch` Subclasses](public_subclasses.md).

## NMDC Search Base

The foundational class for cross-collection queries and linked-instance retrieval.
Use this class for custom workflows that span multiple schema classes.

::: nmdc_client.nmdc_search.NMDCSearch

## Collection Search Base

Extends `NMDCSearch` with collection-focused query helpers.
Use this class for generic collection operations, or use [`CollectionSearch` Subclasses](public_subclasses.md) for preconfigured collection targets.

::: nmdc_client.collection_search.CollectionSearch

## Functional Search

Provides search utilities focused on functional annotation and related retrieval patterns.

::: nmdc_client.functional_search.FunctionalSearch

## Latitude and Longitude Utilities

Provides geospatial helper methods for lat/lon-based filtering and coordinate handling.

::: nmdc_client.lat_long_filters.LatLongFilters

## General Utilities

General-purpose helper utilities used across workflows.

::: nmdc_client.utils.Utils
