# -*- coding: utf-8 -*-
import json
import logging
import unittest
from unittest.mock import MagicMock, patch

import pytest

from nmdc_client.collecting_biosamples_from_site_search import (
    CollectingBiosamplesFromSiteSearch,
)
from nmdc_client.collection_search import CollectionSearch
from nmdc_client.config import API_BASE_URL
from nmdc_client.data_generation_search import DataGenerationSearch
from nmdc_client.data_object_search import DataObjectSearch
from nmdc_client.material_processing_search import MaterialProcessingSearch
from nmdc_client.storage_process_search import StorageProcessSearch
from nmdc_client.study_search import StudySearch
from nmdc_client.workflow_execution_search import WorkflowExecutionSearch

logger = logging.getLogger(__name__)


class TestCollection(unittest.TestCase):
    """
    A class to test each endpoint in the CollectionSearch class.
    """

    def test_get_records(self):
        # simple test to check if the get_records method returns a list of records
        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)
        results = collection.get_records(max_page_size=10, all_pages=False)
        assert isinstance(results, list) and all(
            isinstance(item, dict) for item in results
        )
        assert len(results) == 10

    def test_shape_parameter_does_not_exist(self):
        """
        Test whether specific methods (still) have a parameter named `shape`.
        """

        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)
        with pytest.raises(TypeError):
            collection.get_records(shape="records")
        with pytest.raises(TypeError):
            collection.get_record_by_filter(
                filter='{"id": "nmdc:sty-11-8fb6t785"}', shape="records"
            )
        with pytest.raises(TypeError):
            collection.get_record_by_attribute(
                "name",
                "Lab enrichment of tropical soil microbial communities from Luquillo Experimental Forest, Puerto Rico",
                shape="records",
            )
        with pytest.raises(TypeError):
            collection.get_record_by_id(
                record_id="nmdc:sty-11-8fb6t785", shape="records"
            )

    def test_get_record_by_filter(self):
        # simple test to check if the get_record_by_filter method returns a record
        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)
        results = collection.get_record_by_filter(
            filter='{"id": "nmdc:sty-11-8fb6t785"}'
        )
        assert results[0]["id"] == "nmdc:sty-11-8fb6t785"
        assert len(results) == 1

    def test_get_record_by_attribute(self):
        # simple test to check if the get_record_by_attribute method returns a record
        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)
        results = collection.get_record_by_attribute(
            "name",
            "Lab enrichment of tropical soil microbial communities from Luquillo Experimental Forest, Puerto Rico",
        )
        assert len(results) == 1

    def test_build_filter(self):
        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)

        exact_filter = collection.build_filter(
            attributes={"name": "my record"},
            exact_match=True,
        )
        assert json.loads(exact_filter) == {"name": "my record"}

        partial_filter = collection.build_filter(
            attributes={"name": "GC-MS (2009)"},
            exact_match=False,
        )
        assert partial_filter == (
            '{"name":{"$regex":"GC\\\\-MS\\\\ \\\\(2009\\\\)","$options":"i"}}'
        )
        assert json.loads(partial_filter) == {
            "name": {"$regex": r"GC\-MS\ \(2009\)", "$options": "i"}
        }

    def test_get_record_by_id(self):
        # simple test to check if the get_record_by_id method returns a record
        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)
        results = collection.get_record_by_id("nmdc:sty-11-8fb6t785")
        assert results[0]["id"] == "nmdc:sty-11-8fb6t785"

    def test_get_record_by_id_params(self):
        # simple test to check if the get_record_by_id method returns a record for the two id parameters (record_id (current), collection_id (deprecated))
        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)

        with pytest.warns(DeprecationWarning, match="record_id"):
            results_collect_id = collection.get_record_by_id(
                collection_id="nmdc:sty-11-8fb6t785"
            )
        assert results_collect_id[0]["id"] == "nmdc:sty-11-8fb6t785"

        results_record_id = collection.get_record_by_id(
            record_id="nmdc:sty-11-8fb6t785"
        )
        assert results_record_id[0]["id"] == "nmdc:sty-11-8fb6t785"

        with pytest.raises(ValueError, match="Both.*record_id.*collection_id"):
            collection.get_record_by_id(
                record_id="nmdc:sty-11-8fb6t785",
                collection_id="nmdc:sty-11-8fb6t785",
            )

    def test_check_ids_exist(self):
        # simple test to check if the check_ids_exist method returns a boolean
        collection = CollectionSearch("study_set", api_base_url=API_BASE_URL)
        results = collection.check_ids_exist(["nmdc:sty-11-8fb6t785"])
        assert results == True

    def test_check_ids_exist_multiple(self):
        # simple test to check if the check_ids_exist method returns a boolean
        ids = [
            "nmdc:bsm-11-002vgm56",
            "nmdc:bsm-11-006pnx90",
            "nmdc:bsm-11-00dkyf35",
            "nmdc:bsm-11-00hrxp98",
            "nmdc:bsm-11-00m15h97",
            "nmdc:bsm-11-00yhef97",
            "nmdc:bsm-11-011z7z70",
            "nmdc:bsm-11-0169zs66",
            "nmdc:bsm-11-01bbrr08",
            "nmdc:bsm-11-01f6m423",
            "nmdc:bsm-11-01g9wf51",
            "nmdc:bsm-11-01teww33",
            "nmdc:bsm-11-024rsd62",
            "nmdc:bsm-11-02kcw433",
            "nmdc:bsm-11-02n85875",
            "nmdc:bsm-11-02v78297",
            "nmdc:bsm-11-02x97z84",
            "nmdc:bsm-11-034x5t48",
        ]
        # ids = ['nmdc:bsm-11-002vgm56','nmdc:bsm-11-006pnx90']
        collection = CollectionSearch("biosample_set", api_base_url=API_BASE_URL)
        results = collection.check_ids_exist(ids)
        assert results == True


def _request_params(client) -> dict:
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"resources": []}
        mock_get.return_value.raise_for_status.return_value = None
        client.get_records(all_pages=False)
        return mock_get.call_args.kwargs["params"]


@pytest.mark.parametrize(
    ("client", "expected"),
    [
        (
            WorkflowExecutionSearch(api_base_url=API_BASE_URL),
            {"include_superseded": True, "include_failed": True},
        ),
        (
            DataObjectSearch(
                api_base_url=API_BASE_URL, include_superseded_records=False
            ),
            {"include_superseded": False},
        ),
        (
            DataGenerationSearch(
                api_base_url=API_BASE_URL, include_failed_records=False
            ),
            {"include_failed": False},
        ),
        (
            MaterialProcessingSearch(api_base_url=API_BASE_URL),
            {"include_failed": True},
        ),
        (
            StorageProcessSearch(api_base_url=API_BASE_URL),
            {"include_failed": True},
        ),
        (
            CollectingBiosamplesFromSiteSearch(api_base_url=API_BASE_URL),
            {"include_failed": True},
        ),
        (StudySearch(api_base_url=API_BASE_URL), {}),
    ],
)
def test_include_flags_follow_the_collection(client, expected):
    params = _request_params(client)
    for key in ("include_superseded", "include_failed"):
        if key in expected:
            assert params[key] is expected[key]
        else:
            assert key not in params


def test_get_records_forwards_include_flags_on_later_pages():
    page_one = MagicMock()
    page_one.raise_for_status.return_value = None
    page_one.json.return_value = {
        "resources": [{"id": "nmdc:wfnom-11-x9tbwk91.2"}],
        "next_page_token": "next",
    }
    page_two = MagicMock()
    page_two.raise_for_status.return_value = None
    page_two.json.return_value = {"resources": [{"id": "nmdc:wfnom-11-x9tbwk91.1"}]}

    with patch("requests.get", side_effect=[page_one, page_two]) as mock_get:
        collection = CollectionSearch(
            "workflow_execution_set",
            api_base_url=API_BASE_URL,
            include_superseded_records=False,
            include_failed_records=False,
        )
        results = collection.get_records()

    assert [row["id"] for row in results] == [
        "nmdc:wfnom-11-x9tbwk91.2",
        "nmdc:wfnom-11-x9tbwk91.1",
    ]
    continuation = mock_get.call_args_list[1].kwargs["params"]
    assert continuation["include_superseded"] is False
    assert continuation["include_failed"] is False
    assert continuation["page_token"] == "next"


def test_include_flags_rejected_when_the_collection_has_no_such_records():
    with pytest.raises(ValueError, match="include_superseded_records"):
        CollectionSearch(
            "study_set",
            api_base_url=API_BASE_URL,
            include_superseded_records=False,
        )
    with pytest.raises(ValueError, match="include_failed_records"):
        CollectionSearch(
            "data_object_set",
            api_base_url=API_BASE_URL,
            include_failed_records=False,
        )
    with pytest.raises(TypeError):
        DataObjectSearch(api_base_url=API_BASE_URL, include_failed_records=False)
    with pytest.raises(TypeError):
        StudySearch(api_base_url=API_BASE_URL, include_superseded_records=False)


def test_superseded_workflow_execution_is_omitted_from_id_search():
    # nmdc:wfnom-11-x9tbwk91.1 is superseded by nmdc:wfnom-11-x9tbwk91.2.
    # Prod still returns both ids, so this fails there until that Runtime release.
    search = WorkflowExecutionSearch(
        api_base_url=API_BASE_URL,
        include_superseded_records=False,
    )
    ids = {
        row["id"]
        for row in search.get_record_by_attribute(
            "id",
            "nmdc:wfnom-11-x9tbwk91",
            fields="id",
        )
    }
    assert "nmdc:wfnom-11-x9tbwk91.2" in ids
    assert "nmdc:wfnom-11-x9tbwk91.1" not in ids
