# -*- coding: utf-8 -*-
import json
import logging
import unittest

import pytest

from nmdc_client.collection_search import CollectionSearch
from nmdc_client.config import API_BASE_URL
from nmdc_client.data_generation_search import DataGenerationSearch
from nmdc_client.data_object_search import DataObjectSearch
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


def _record_ids(search, value, **kwargs):
    return {
        row["id"]
        for row in search.get_record_by_attribute("id", value, fields="id", **kwargs)
    }


WORKFLOW_STEM = "nmdc:wfnom-11-x9tbwk91"
SUPERSEDED_WORKFLOW = "nmdc:wfnom-11-x9tbwk91.1"
CURRENT_WORKFLOW = "nmdc:wfnom-11-x9tbwk91.2"
SUPERSEDED_DATA_OBJECTS = ("nmdc:dobj-11-002stx72", "nmdc:dobj-11-003x7710")
FAILED_DATA_GENERATION = "nmdc:dgns-11-41509674"


def test_workflow_execution_id_search_includes_superseded_record_by_default():
    ids = _record_ids(WorkflowExecutionSearch(api_base_url=API_BASE_URL), WORKFLOW_STEM)
    assert CURRENT_WORKFLOW in ids
    assert SUPERSEDED_WORKFLOW in ids


def test_superseded_workflow_execution_is_omitted_from_id_search():
    ids = _record_ids(
        WorkflowExecutionSearch(
            api_base_url=API_BASE_URL,
            include_superseded_records=False,
        ),
        WORKFLOW_STEM,
    )
    assert CURRENT_WORKFLOW in ids
    assert SUPERSEDED_WORKFLOW not in ids


def test_superseded_data_object_follows_include_flag():
    # Prod still returns superseded data objects when the flag is false.
    data_object_id = SUPERSEDED_DATA_OBJECTS[0]
    assert data_object_id in _record_ids(
        DataObjectSearch(api_base_url=API_BASE_URL),
        data_object_id,
        exact_match=True,
    )
    assert data_object_id not in _record_ids(
        DataObjectSearch(api_base_url=API_BASE_URL, include_superseded_records=False),
        data_object_id,
        exact_match=True,
    )


def test_failed_data_generation_follows_include_flag():
    # nmdc:dgns-11-41509674 has qc_status fail.
    assert FAILED_DATA_GENERATION in _record_ids(
        DataGenerationSearch(api_base_url=API_BASE_URL),
        FAILED_DATA_GENERATION,
        exact_match=True,
    )
    assert FAILED_DATA_GENERATION not in _record_ids(
        DataGenerationSearch(api_base_url=API_BASE_URL, include_failed_records=False),
        FAILED_DATA_GENERATION,
        exact_match=True,
    )


def test_superseded_data_objects_span_pages():
    search = DataObjectSearch(
        api_base_url=API_BASE_URL, include_superseded_records=True
    )
    rows = search.get_record_by_filter(
        json.dumps({"id": {"$in": list(SUPERSEDED_DATA_OBJECTS)}}),
        max_page_size=1,
        fields="id",
    )
    assert {row["id"] for row in rows} == set(SUPERSEDED_DATA_OBJECTS)
