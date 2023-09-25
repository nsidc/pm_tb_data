# PM Data Products Notes

TODO: add notes about what products and resolutions are most appropriate for
different products (e.g., SIC, snow extent, etc.).

## Near real time LANCE data for AMSR2

[Link to data (requires earthdata login)](https://lance.nsstc.nasa.gov/amsr2-science/data/level3/seaice12/R04/hdfeos5/)
[Link to dataset landing page](https://cmr.earthdata.nasa.gov/search/concepts/C1886605827-LANCEAMSR2.html#)

* `*_P04_*` files are "NRT". Usually only one P file at a time. If data never completes for a day, P file remains.
* `*_R04_*` files are "final".
* Sometimes no file for a day at all.

Data are updated throughout the day – as new swaths become available – as
“…P04…” files.

Usually, these P04 files are replaced with “R04” files once the next day’s
processing begins. However, sometimes no R04 file gets created and the only file
available for a day is the (last) P04 file.

Even more rarely, no data is available ever for a day, and there is no file for
that date…ie no P04 file and no R04 file.

The ECDR will only use “completed day” sets of data, this means that the latest
day for which we can use these NRT data is the day before the latest day
available from this site.

To recap, that latest-day will usually be a “R04” file, will sometimes be a
“P04” file and will rarely be missing entirely.
