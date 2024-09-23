import datetime as dt

from pm_tb_data.fetch.nsidc_0080 import get_nsidc_0080_tbs_from_disk


def test_get_nsidc_0080_tbs_from_disk():
    tbs = get_nsidc_0080_tbs_from_disk(
        hemisphere="north",
        # Look 3 days in the past. There should be data for this date.
        # TODO: consider getting a listing (or searching CMR) to find out what
        # the lastest date of data is and read that in. NRT can be a little
        # unpredictable since data roll off and the latest might be impacted by
        # processing delays or a platform going offline.
        date=dt.date.today() - dt.timedelta(3),
        resolution="25",
        platform_id="F18",
    )

    assert "h19" in tbs
