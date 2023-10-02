<p float="left">
    <img alt="NSIDC logo" src="https://nsidc.org/themes/custom/nsidc/logo.svg" width="150" />
    <img alt="NOAA@NSIDC logo" src="https://nsidc.org/sites/default/files/images/Logo/noaa_at_nsidc.png" width="150" />
    <img alt="NASA logo" src="https://gpm.nasa.gov/sites/default/files/document_files/NASA-Logo-Large.png" width="150" />
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

### Adding dependencies

To add new dependencies to this project, update the `environment.yml` file with
the new dependency. Then update your conda environment:

```
$ mamba env update
```

Once the conda environment has been updated, lock the environment using `conda-lock`:

```
$ conda-lock
```

Commit the changes for the `environment.yml` and the `conda-lock.yml` files.


### Running tests/CI

This project uses [pre-commit](https://pre-commit.com/) to run pre-commit hooks
that check and format this project's code for stylistic consistency (using
`ruff` and `black`) and perform typechecking (`mypy`).

The pre-commit configuration for this project can be found in
`.pre-commit-config.yaml`. Configuration for specific tools (e.g., `mypy`) is
given in the included `pyproject.toml`.

For more information about using `pre-commit`, please sese the [Scientific
Python Library Development Guide's section on
pre-commit](https://learn.scientific-python.org/development/guides/gha-basic/#pre-commit).

To install pre-commit to run checks for each commit you make:

```
$ pre-commit install
```

To manually run the pre-commit hooks without a commit:

```
$ pre-commit run --all-files
```

### Creating a new version

Use `bumpversion` (see
[bump-my-version](https://github.com/callowayproject/bump-my-version)) to bump
the specified part of the version:

```
$ bumpversion bump {major|minor|patch}
```

`bumpversion` configuration can be found in the `pyproject.toml`.


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
