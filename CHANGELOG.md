# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-02-21

### Added

- Fallback `TimeUtilities` class implementation in `pyiri2016/__init__.py` for robustness when `timeutil` package is unavailable
- Explicit dependency declaration for `timeutil` package from GitHub in `pyproject.toml`

### Fixed

- Fixed `NameError: name 'TimeUtilities' is not defined` when `timeutil` package was not installed
- Updated imports in `pyiri2016/iri2016prof2D.py` to use fallback `TimeUtilities` if external package is missing

### Changed

- Raised minimum Python version requirement to 3.11
- Updated `pyproject.toml` to explicitly include `timeutil @ git+https://github.com/rilma/TimeUtilities.git` as a project dependency

### Removed

- **Obsolete Poetry-era build files**: `build_helper.py`, `pyproject_build_hook.py`, `poetry.lock`
- **Alternative build system**: `meson.build` (root, `pyiri2016/`, `source/`)
- **Deprecated CI configuration**: `.travis.yml` (replaced by GitHub Actions)
- **CodeClimate configuration**: `.codeclimate.yml` (unused)
- **Build artifacts**: `build/`, `dist/`, `pyiri2016.egg-info/` directories (now properly gitignored)
- **Generated files**: `.coverage` (coverage cache file)
- **Migration-related artifacts**: `verify_migration.sh`, `.ansible/poetry.yaml`
- **Redundant configuration**: `setup.cfg` (minimal content consolidated into `setup.py`)

## [1.1.0] - 2017-01-12

### Added

- [ISSUE 18](https://github.com/rilma/pyIRI2016/issues/18) Retrieval of `Fortran`, coefficients, and indices files
- [ISSUE 13](https://github.com/rilma/pyIRI2016/issues/13) `Python` + `Fortran` in a `Docker` image for `f2py`, or better
- [ISSUE 14](https://github.com/rilma/pyIRI2016/issues/14) Release a `CHANGELOG`
- Comprehensive `README` file
- Installation through `setuptools`
- Unit-testing case
- API implementation in `pyiri2016.IRI2016` class
- `Travis` CI script

### Changed

- [ISSUE 16](https://github.com/rilma/pyIRI2016/issues/16) Set `main` as default branch

### Fixed
