<p float="left" align="center">
    <img alt="NSIDC logo" src="https://nsidc.org/themes/custom/nsidc/logo.svg" height="150" />
    <img alt="NOAA@NSIDC logo" src="https://nsidc.org/sites/default/files/images/Logo/noaa_at_nsidc.png" height="150" />
    <img alt="NASA logo" src="https://gpm.nasa.gov/sites/default/files/document_files/NASA-Logo-Large.png" height="150" />
</p>

# NSIDC Passive Microwave Brightness Temperatures Data python libarary

The `pm_tb_data` python library enables users to access passive microwave data
from NSIDC in a consistent manner. This libarary exposes standard data models
for passive microwave data that are expected by other libraries that consume
passive microwave data at NSIDC (e.g., [`pm_icecon`](https://github.com/nsidc/pm_icecon).

Please note that this repository is a work in progress and breaking changes are
to be expected. Initial work on this repository is specific to NSIDC's internal
systems and may not work as expected for external collaborators.

## Requirements and installation

This code relies on the python packages defined in the included
`environment.yml` file.

Use [conda](https://docs.conda.io/en/latest/) or
[mamba](https://mamba.readthedocs.io/en/latest/index.html) to install the
requirements:

```
$ conda env create
```

To activate the environment:

```
$ conda activate pm_tb_data
```

## Usage

TODO

## Development/contributing

See [doc/development.md](doc/development.md) for more information.

## Level of Support

* This repository is not actively supported by NSIDC but we welcome issue submissions and
  pull requests in order to foster community contribution.

See the [LICENSE](LICENSE) for details on permissions and warranties. Please contact
nsidc@nsidc.org for more information.


## License

See [LICENSE](LICENSE).


## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).


## Credit

This software was developed by the National Snow and Ice Data Center with
funding from NASA and NOAA.
