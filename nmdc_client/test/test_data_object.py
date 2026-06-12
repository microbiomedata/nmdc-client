# -*- coding: utf-8 -*-
import logging

from nmdc_client import DataObjectSearch
from nmdc_client.config import API_BASE_URL

logger = logging.getLogger(__name__)


def test_get_data_objects_for_study():
    """
    Test the get_data_objects_for_study method.
    """
    do_search = DataObjectSearch(api_base_url=API_BASE_URL)

    study_id = "nmdc:sty-11-aygzgv51"
    results = do_search.get_data_objects_for_study(study_id)
    logger.debug(f"Results: {results}")
    assert results
    assert len(results) > 0
    assert "data_objects" in results[0]


def test_get_data_objects_for_studies():
    """
    Test the (deprecated) get_data_objects_for_studies (plural) method.
    """
    do_search = DataObjectSearch(api_base_url=API_BASE_URL)

    study_id = "nmdc:sty-11-aygzgv51"
    results = do_search.get_data_objects_for_studies(study_id)
    logger.debug(f"Results: {results}")
    assert results
    assert len(results) > 0
    assert "data_objects" in results[0]
