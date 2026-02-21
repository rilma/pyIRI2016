# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Plotting dependencies** (issue #28): Added optional `plotting` extras for matplotlib-based visualization
  - matplotlib, scipy, basemap-data, basemap, seaborn
  - Install with: `pip install pyiri2016[plotting]`
- **Demo script for saving plots** (issue #28): `examples/demo_save_plots.py` shows how to save plotting examples to PNG files
  - Useful for headless environments and CI/CD pipelines
  - Run with: `make demo-plots`
- **Optional dependency handling**: Made `pyapex` and `pyigrf` optional with graceful error messages when attempting advanced features
  - `LatVsFL()` requires pyapex (install with: `pip install pyapex`)
  - IGRF magnetic field calculations require pyigrf (install with: `pip install pyigrf`)
- **CMake build system** (issue #26): Modern CMake 3.15+ configuration for cross-platform builds
- **scikit-build-core backend**: PEP 517/518 compliant build system replacing deprecated numpy.distutils
- **generate_f2py.py**: Python wrapper script for f2py module generation with proper error handling
- **f2py_wrapper.sh**: Shell wrapper for setting UTF-8 environment variables during Fortran compilation
- **Enhanced Makefile targets**:
  - `make clean-venv`: Remove and rebuild virtual environment from scratch
  - `make coverage`: Generate pytest coverage reports with HTML output
  - `make test-examples`: Test all example scripts (1D plotting and 2D mapping examples)
  - Better separation between `make dev` (development) and `make install` (user installation)
- **.gitignore enhancements**: Added `.venv/`, `.pytest_cache/`, `htmlcov/` for cleaner repository
- **Updated GitHub Actions workflow**: Replaced uv package manager with system dependencies (gfortran, cmake)

### Changed

- **pyproject.toml**: Added optional `plotting` extras group with visualization dependencies; added `packaging>=24.0` to build requirements
- **Makefile**: Split `dev` and `dev-plotting` targets for separate development environments; added `packaging>=24.0` to pip upgrades
- **iri2016prof2D.py**: Made `pyapex` and `pyigrf` optional imports with graceful error handling
- **NumPy upgrade** (issue #29): Upgraded from numpy<2.0 to numpy>=2.0 (latest version supported under Python 3.11)
  - Updated all build and runtime configurations to support NumPy 2.0+
  - Requires Python 3.11+ (already enforced)
- **Build system**: Migrated from `setup.py` + `numpy.distutils` to `CMakeLists.txt` + `scikit-build-core`
- **Documentation**: 
  - Updated README.md with modern build system instructions
  - Completely rewrote QUICKSTART.md with CMake-specific guidance
  - Removed references to deprecated uv package manager
- **Fortran source files**: Fixed UTF-8 encoding in `source/irifun.for` by converting to ASCII-compatible format
- **Environment handling**: UTF-8 encoding now managed by Makefile exports, f2py_wrapper.sh, and CMakeLists.txt

### Removed

- **setup.py**: Legacy file using deprecated numpy.distutils (replaced by CMakeLists.txt + pyproject.toml)
- **uv.lock**: Lock file from old uv package manager
- **.env**: Environment file (UTF-8 encoding now handled by build infrastructure)
- **Temporary migration files**:
  - `CMAKE_MIGRATION_NOTES.md`: Temporary documentation from migration process
  - `validate_build_env.py`: Temporary validation script (replaced by `make health`)
  - `test_build.sh`: Temporary test script (replaced by Makefile targets)

### Fixed

- **UTF-8 encoding issue** in Fortran source parsing: f2py now correctly handles non-ASCII characters through proper environment variable propagation
- **GitHub Actions workflow**: Updated to work with new CMake-based build system
- **Plotting examples** (issue #28): Added missing dependencies and created `make test-examples` target for testing

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
