[![alt tag](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)
[![Smoke](https://github.com/rilma/pyIRI2016/actions/workflows/smoke.yml/badge.svg?branch=main)](https://github.com/rilma/pyIRI2016/actions/workflows/smoke.yml)

# pyIRI2016

![alt tag](figures/iri2DExample02.gif)

Python wrapper to the [International Reference Ionosphere (IRI) 2016 model](http://irimodel.org/). 


## Installing

    pip install pyiri2016

Or
```sh
pip install -e .
```
This also installs [Time Utilities](https://github.com/rilma/TimeUtilities).

## Development Setup

This project uses a modern CMake-based build system with scikit-build-core for cross-platform compilation.

For detailed setup instructions, build troubleshooting, and advanced configuration, see [QUICKSTART.md](QUICKSTART.md).

### Quick Start
```sh
# Create venv and install dependencies with Fortran extension
make dev
```

This target:
- Creates `.venv` virtual environment
- Installs NumPy, scikit-build-core, CMake, Ninja
- Compiles and installs the package in editable mode
- Installs development tools (pytest, coverage, pre-commit)

**Expected time**: 2-5 minutes on first run (gfortran compilation)

### Build Distribution Packages
```sh
make build
```

Creates source distribution and binary wheel in `dist/` directory.

## Test

```sh
make health
make smoke
make test
```

`make smoke` runs a fast, CI-safe syntax check without network or Fortran build requirements.
`make health` verifies Python, gfortran, and cmake are available, then runs `make smoke`.

## Examples

For running examples and plotting demonstrations, see [examples/README.md](examples/README.md).

Example outputs:

| | |
|---|---|
| ![Height Profile](figures/iri1DExample01.png) | ![Latitude Profile](figures/iri1DExample02.png) |
| ![Time Profile](figures/iri1DExample08.png) | ![Height vs Time](figures/iri2DExample01.png) |

## Reference

### Build System Architecture

The build system uses:
- **CMakeLists.txt**: Modern CMake 3.15+ configuration for cross-platform builds
- **generate_f2py.py**: Python wrapper that generates f2py C/Fortran interface code
- **f2py_wrapper.sh**: Shell wrapper ensuring UTF-8 environment variables are set for f2py
- **pyproject.toml**: PEP 517/518 compliant build system using scikit-build-core

The system automatically handles:
- Fortran source compilation with gfortran
- f2py wrapper generation (only wraps `iriwebg` subroutine as public interface)
- NumPy integration for array handling
- UTF-8 encoding for source files with non-ASCII characters

For advanced build control, see `CMakeLists.txt` and `generate_f2py.py`.
