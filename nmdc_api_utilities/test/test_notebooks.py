# -*- coding: utf-8 -*-
from nmdc_api_utilities import DataObjectSearch, WorkflowExecutionSearch
from nmdc_api_utilities.config import API_BASE_URL


def test_nom_notebook():
    dos_client = DataObjectSearch(api_base_url=API_BASE_URL)

    processed_nom = dos_client.get_record_by_attribute(
        attribute_name="data_object_type",
        attribute_value="Direct Infusion FT-ICR MS Analysis Results",
        max_page_size=100,
        fields="id,md5_checksum,url",
        all_pages=True,
    )
    # clarify names
    for dataobject in processed_nom:
        dataobject["processed_nom_id"] = dataobject.pop("id")
        dataobject["processed_nom_md5_checksum"] = dataobject.pop("md5_checksum")
        dataobject["processed_nom_url"] = dataobject.pop("url")

    # convert to df

    # since we are querying the WorkflowExecution collection, we need to create an instance of it
    we_client = WorkflowExecutionSearch(api_base_url=API_BASE_URL)
    # use utility function to get a list of the ids from processed_nom
    result_ids = [data_object["processed_nom_id"] for data_object in processed_nom]
    # get the analysis data objects
    analysis_dataobj = we_client.get_batch_records(
        id_list=result_ids,
        search_field="has_output",
        fields="id,has_input,has_output",
        chunk_size=100,
    )

    # clarify names
    for dataobject in analysis_dataobj:
        dataobject["analysis_id"] = dataobject.pop("id")
        dataobject["analysis_has_input"] = dataobject.pop("has_input")
        dataobject["analysis_has_output"] = dataobject.pop("has_output")

    assert len(analysis_dataobj) > 2000
