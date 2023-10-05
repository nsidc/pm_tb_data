"""Tests related to AMSR2 LANCE data."""
import datetime as dt

import pm_tb_data.fetch.nrt as nrt


def test__filter_out_last_day():
    latest_date = dt.date(2023, 10, 5)
    second_date = latest_date - dt.timedelta(days=1)
    third_date = latest_date - dt.timedelta(days=2)
    mock_granules: nrt.GranuleInfoByDate = {
        latest_date: {
            "file_type": "P04",
            "filename": "AMSR_U2_L3_SeaIce12km_P04_20231005.he5",
            "data_url": "www.example.com",
        },
        second_date: {
            "file_type": "R04",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231004.he5",
            "data_url": "www.example.com",
        },
        third_date: {
            "file_type": "R04",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231003.he5",
            "data_url": "www.example.com",
        },
    }

    filtered = nrt._filter_out_last_day(granules_by_date=mock_granules)
    assert latest_date not in filtered.keys()
    assert second_date in filtered.keys()
    assert third_date in filtered.keys()


def test__filter_out_last_day_unless_r04():
    latest_date = dt.date(2023, 10, 5)
    second_date = latest_date - dt.timedelta(days=1)
    third_date = latest_date - dt.timedelta(days=2)
    mock_granules: nrt.GranuleInfoByDate = {
        latest_date: {
            "file_type": "R04",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231005.he5",
            "data_url": "www.example.com",
        },
        second_date: {
            "file_type": "R04",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231004.he5",
            "data_url": "www.example.com",
        },
        third_date: {
            "file_type": "R04",
            "filename": "AMSR_U2_L3_SeaIce12km_R04_20231003.he5",
            "data_url": "www.example.com",
        },
    }

    filtered = nrt._filter_out_last_day(granules_by_date=mock_granules)
    assert latest_date in filtered.keys()
    assert second_date in filtered.keys()
    assert third_date in filtered.keys()
