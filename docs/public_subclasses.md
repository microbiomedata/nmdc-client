# `CollectionSearch` Subclasses

Collection-specific subclasses are the recommended public entry points.
Each class inherits `CollectionSearch` behavior while preconfiguring a collection target.

## Choosing a Subclass

- Pick the subclass matching the record type you want to query.
- Use inherited methods such as `get_record_by_id`, `get_record_by_attribute`, `get_record_by_filter`, and `get_records`.
- See [Using MongoDB Filters](filters.ipynb) for query construction and operator examples.
- NMDC Schema reference: <https://microbiomedata.github.io/nmdc-schema/>
- Typecode-to-class map: <https://microbiomedata.github.io/nmdc-schema/typecode-to-class-map/>

## Biosample and Study Related

These classes focus on study-level and site-level discovery.
Use them when starting from study metadata, biosamples, or collection events.

::: nmdc_client.biosample_search.BiosampleSearch

::: nmdc_client.study_search.StudySearch

::: nmdc_client.collecting_biosamples_from_site_search.CollectingBiosamplesFromSiteSearch

::: nmdc_client.field_research_site_search.FieldResearchSiteSearch

## Sample Processing Related

These classes target records produced through sample processing lifecycle, including processed sample entities and upstream material/storage processes.
Use NMDC Schema docs to confirm class semantics and filterable fields.

::: nmdc_client.processed_sample_search.ProcessedSampleSearch

::: nmdc_client.material_processing_search.MaterialProcessingSearch

::: nmdc_client.storage_process_search.StorageProcessSearch

## Data Generation Related

These classes cover records tied to generation setup and instrumentation.
Use schema and typecode map when selecting classes for linked-instance queries.

::: nmdc_client.data_generation_search.DataGenerationSearch

::: nmdc_client.manifest_search.ManifestSearch

::: nmdc_client.instrument_search.InstrumentSearch

::: nmdc_client.configuration_search.ConfigurationSearch

## Data and Processing Related

These classes are useful for workflow context, calibration context, data objects, and functional annotation aggregation outputs.
Use NMDC Schema docs for exact field meanings and schema class names.

::: nmdc_client.workflow_execution_search.WorkflowExecutionSearch

::: nmdc_client.calibration_search.CalibrationSearch

::: nmdc_client.data_object_search.DataObjectSearch

::: nmdc_client.functional_annotation_agg_search.FunctionalAnnotationAggSearch
