## 0.6.0

* Add support for fetching data from NSIDC0802 from disk.

## 0.5.0

* Add support for fetching data from NSIDC0080 from disk.


## 0.4.0

* Update `earthaccess` library version to `~=0.8.2`.
* The code that downloads `AU_SI12_NRT_R04` LANCE NRT data
  (``pm_tb_data.fetch.amsr.lance_amsr2`) 
    * now supports trying both data URLs provided by CMR (lance.nsstc.nasa.gov
      and lance.itsc.uah.edu) if the first one fails. Sometimes one mirror is
      available when the other is not.
    * Writes partially-downloaded data to a tempdir. Once the data is fully
      downloaded, the data are moved to the expected output dir. This prevents
      network interruptions from resulting in partially-written data.

## 0.3.0

* Add code to fetch NSIDC-0001 v6 data from disk.
* Add code to fetch AE_SI12 v3 from disk.
* `AU_SI`, `AE_SI`, and `NSIDC-0001` data normalization produces 'standard'
  xarray dataset: variables are named in a consistent way, and variables all
  have just two dims: `fake_x` and `fake_y`. Eventually the plan is to include
  CRS information and projected coordinates instead.


## 0.2.0

* Add code to download LANCE AMSR2 data to a local directory.
* Define type and constants for `Hemisphere`.


## v0.1.2

* Fix package build: use the `setuptools` `find` directive to automatically find
  packages within `pm_tb_data`.

## v0.1.1

* Add `py.typed` to built package-data.

## v0.1.0

* Initial release of `pm_tb_data`. Most of the code included here is originally
  from `pm_icecon` v0.1.0.
