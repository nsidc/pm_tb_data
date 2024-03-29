"""Tests related to AMSR2 LANCE data."""

import datetime as dt

import pytest

import pm_tb_data.fetch.amsr.lance_amsr2 as lance_amsr2
from pm_tb_data.fetch.errors import FetchRemoteDataError


def test__filter_out_last_day():
    latest_date = dt.date(2023, 10, 5)
    second_date = latest_date - dt.timedelta(days=1)
    third_date = latest_date - dt.timedelta(days=2)
    mock_granules: lance_amsr2.GranuleInfoByDate = {
        latest_date: {
            "file_type": "P",
            "filename": "AMSR_U2_L3_SeaIce12km_P04_20231005.he5",
            "data_urls": ["www.example.com"],
        },
        second_date: {
            "file_type": "R",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231004.he5",
            "data_urls": ["www.example.com"],
        },
        third_date: {
            "file_type": "R",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231003.he5",
            "data_urls": ["www.example.com"],
        },
    }

    filtered = lance_amsr2._filter_out_last_day(granules_by_date=mock_granules)
    assert latest_date not in filtered.keys()
    assert second_date in filtered.keys()
    assert third_date in filtered.keys()


def test__filter_out_last_day_unless_r04():
    latest_date = dt.date(2023, 10, 5)
    second_date = latest_date - dt.timedelta(days=1)
    third_date = latest_date - dt.timedelta(days=2)
    mock_granules: lance_amsr2.GranuleInfoByDate = {
        latest_date: {
            "file_type": "R",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231005.he5",
            "data_urls": ["www.example.com"],
        },
        second_date: {
            "file_type": "R",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231004.he5",
            "data_urls": ["www.example.com"],
        },
        third_date: {
            "file_type": "R",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231003.he5",
            "data_urls": ["www.example.com"],
        },
    }

    filtered = lance_amsr2._filter_out_last_day(granules_by_date=mock_granules)
    assert latest_date in filtered.keys()
    assert second_date in filtered.keys()
    assert third_date in filtered.keys()


def test__filter_out_last_day_with_gap_r04():
    latest_date = dt.date(2023, 10, 5)
    second_date = latest_date - dt.timedelta(days=2)
    third_date = latest_date - dt.timedelta(days=3)
    mock_granules: lance_amsr2.GranuleInfoByDate = {
        latest_date: {
            "file_type": "P",
            "filename": "AMSR_U2_L3_SeaIce12km_P04_20231005.he5",
            "data_urls": ["www.example.com"],
        },
        second_date: {
            "file_type": "R",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231003.he5",
            "data_urls": ["www.example.com"],
        },
        third_date: {
            "file_type": "R",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231002.he5",
            "data_urls": ["www.example.com"],
        },
    }

    filtered = lance_amsr2._filter_out_last_day(granules_by_date=mock_granules)
    assert latest_date not in filtered.keys()
    assert second_date in filtered.keys()
    assert third_date in filtered.keys()


def test__get_granule_info_by_date():
    class MockDataGranule:
        def __init__(self):
            self._filename = "AMSR_U2_L3_SeaIce12km_R04_20231003.he5"

        def __dict__(self):
            return {
                "meta": {
                    "native-id": self._filename,
                }
            }

        def __getitem__(self, *args, **_kwargs):
            return self.__dict__()[args[0]]

        def data_links(self, *args, **_kwargs):
            return [f"www.example.com/foo/{self._filename}"]

    mock_data_granule = MockDataGranule()

    expected = {
        dt.date(2023, 10, 3): {
            "file_type": "R",
            "filename": mock_data_granule._filename,
            "data_urls": [f"www.example.com/foo/{mock_data_granule._filename}"],
        }
    }

    actual = lance_amsr2._get_granule_info_by_date(data_granules=[mock_data_granule])

    assert actual == expected


def test__get_granule_info_by_date_raises_error():
    class MockDataGranule:
        def __dict__(self):
            return {
                "meta": {
                    "native-id": "unexpected_filename.foo",
                }
            }

        def __getitem__(self, *args, **_kwargs):
            return self.__dict__()[args[0]]

    mock_data_granule = MockDataGranule()

    with pytest.raises(FetchRemoteDataError):
        lance_amsr2._get_granule_info_by_date(data_granules=[mock_data_granule])
