# PM Data Products Notes

TODO: add notes about what products and resolutions are most appropriate for
different products (e.g., SIC, snow extent, etc.).

## Near real time LANCE data for AMSR2

[Link to data (requires earthdata login)](https://lance.nsstc.nasa.gov/amsr2-science/data/level3/seaice12/R04/hdfeos5/)
[Link to dataset landing page](https://cmr.earthdata.nasa.gov/search/concepts/C1886605827-LANCEAMSR2.html#)

* `P` files are "partial". These files get updated throughout the day as
  new swaths come in and usually get replaced by an `R` file. If data
  never completes for a day, the `P` file remains.
* `R` files are considered "ready Near-Real-Time (NRT)" for the purposes of the ECDR.
* Sometimes no file for a day at all.

Usually, these `P` files are replaced with `R` files once the next day’s
processing begins. However, sometimes no `R` file gets created and the only file
available for a day is the (last) `P` file.

Even more rarely, no data is available ever for a day, and there is no file for
that date…ie no `P` or `R` file is created.

The ECDR will only use “ready for NRT”/completed day sets of data, this means
that the latest day for which we can use these NRT data is the day before the
latest day available from this site.

To recap, that latest-day will usually be a `R` file, will sometimes be a
`P` file and will rarely be missing entirely.
