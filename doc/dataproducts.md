# PM Data Products Notes

TODO: add notes about what products and resolutions are most appropriate for
different products (e.g., SIC, snow extent, etc.).

## Near real time LANCE data for AMSR2

[Link to data (requires earthdata login)](https://lance.nsstc.nasa.gov/amsr2-science/data/level3/seaice12/R04/hdfeos5/)
[Link to dataset landing page](https://cmr.earthdata.nasa.gov/search/concepts/C1886605827-LANCEAMSR2.html#)

* `*_P04_*` files are "partial". These files get updated throughout the day as
  new swaths come in and usually get replaced by an `*_R04_*` file. If data
  never completes for a day, the `*_P04_*` file remains.
* `*_R04_*` files are considered "ready Near-Real-Time (NRT)" for the purposes of the ECDR.
* Sometimes no file for a day at all.

Usually, these `*_P04_*` files are replaced with `*_R04_*` files once the next day’s
processing begins. However, sometimes no `*_R04_*` file gets created and the only file
available for a day is the (last) `*_P04_*` file.

Even more rarely, no data is available ever for a day, and there is no file for
that date…ie no `*_P04_*` or `*_R04_*` file is created.

The ECDR will only use “ready for NRT”/completed day sets of data, this means
that the latest day for which we can use these NRT data is the day before the
latest day available from this site.

To recap, that latest-day will usually be a `*_R04_*` file, will sometimes be a
`*_P04_*` file and will rarely be missing entirely.
