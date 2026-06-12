# -*- coding: utf-8 -*-
import logging

from nmdc_client import BiosampleSearch
from nmdc_client.config import API_BASE_URL

logger = logging.getLogger(__name__)


def test_find_biosample_by_id():
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_id("nmdc:bsm-11-002vgm56")
    assert len(results) > 0
    assert results[0]["id"] == "nmdc:bsm-11-002vgm56"


def test_logger():
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    logger.basicConfig(level=logging.DEBUG)
    results = biosample.get_record_by_id("nmdc:bsm-11-002vgm56")


def test_biosample_by_filter():
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_filter('{"id":"nmdc:bsm-11-006pnx90"}')
    assert len(results) > 0


def test_biosample_by_attribute():
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_attribute(
        "id", "nmdc:bsm-11-006pnx90", exact_match=False
    )
    logger.debug(results)
    assert len(results) == 1


def test_biosample_by_latitude():
    # {"lat_lon.latitude": {"$gt": 45.0}, "lat_lon.longitude": {"$lt":45}}
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_latitude("gt", 45.0)
    assert len(results) > 0
    assert results[0]["lat_lon"]["latitude"] == 63.875088


def test_biosample_by_longitude():
    # {"lat_lon.latitude": {"$gt": 45.0}, "lat_lon.longitude": {"$lt":45}}
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_longitude("lt", 45.0)
    assert len(results) > 0
    assert results[0]["lat_lon"]["longitude"] == -149.210438


def test_biosample_by_lat_long():
    # {"lat_lon.latitude": {"$gt": 45.0}, "lat_lon.longitude": {"$lt":45}}
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_lat_long("gt", "lt", 45.0, 45.0)
    assert len(results) > 0
    assert results[0]["lat_lon"]["latitude"] == 63.875088
    assert results[0]["lat_lon"]["longitude"] == -149.210438


def test_biosample_by_proximity_biosample():
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_proximity(
        radius_km=1, record_id="nmdc:bsm-11-7bk7nf04"
    )
    assert len(results) > 5


def test_biosample_by_proximity_location():
    biosample = BiosampleSearch(api_base_url=API_BASE_URL)
    results = biosample.get_record_by_proximity(
        radius_km=2180,
        query_lat=65.42577,
        query_lon=-150.416496,
        all_pages=True,
    )
    assert len(results) > 1000
    captured_studies = {
        study_id
        for result in results
        for study_id in result.get("associated_studies", [])
    }
    assert len(captured_studies) > 10
