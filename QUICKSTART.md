# Quick Start - Build and Test

## TL;DR

Just run:
```bash
make dev       # Create venv and build with Fortran extension
make test      # Run test suite with pytest
make build     # Create distribution packages
```

## What's New in v1.2.0

✅ **CMake Build System** - Replaced deprecated numpy.distutils with modern CMake 3.15+ + scikit-build-core  
✅ **TimeUtilities Integration** - Added fallback implementation for robustness  
✅ **Improved Dependency Management** - Explicit `timeutil` package dependency from GitHub  
✅ **Python 3.11+ Minimum** - Raised minimum Python version requirement to 3.11  
✅ **Project Cleanup** - Removed obsolete Poetry/Meson/uv build files  

## Build System Overview

The new build system uses:
- **CMake 3.15+** for cross-platform compilation
- **scikit-build-core** backend (PEP 517/518 compliant)
- **f2py** for Fortran-Python bindings
- **UTF-8 environment variables** for Fortran source handling

Key files:
- `CMakeLists.txt` - Build configuration
- `generate_f2py.py` - f2py wrapper script
- `f2py_wrapper.sh` - Environment setup for UTF-8 encoding
- `pyproject.toml` - Package metadata and build dependencies

## Build Process

### 1. Development Installation

```bash
make dev
```

This target:
- Creates `.venv` virtual environment if needed
- Installs build tools (NumPy, CMake, Ninja, scikit-build-core)
- Installs runtime dependencies (simple-settings, beautifulsoup4, wget, charset-normalizer)
- Compiles Fortran extension (iriweb) with f2py
- Installs package in editable mode (`pip install -e .`)
- Installs development tools (pytest, pytest-cov, coverage, pre-commit, parameterized)

**Expected time**: 2-5 minutes (slower on first run due to gfortran compilation)

### 2. Run Tests

```bash
make test
```

This target:
- Runs pytest on tests directory
- Verbose output with short tracebacks
- Tests module imports and API functionality

**Expected time**: 30 seconds - 2 minutes

### 3. Build Distribution Packages

```bash
make build
```

This target:
- Creates source distribution (sdist)
- Creates binary wheel with compiled Fortran extension
- Packages available in `dist/` directory
- Reproducible across platforms

**Expected time**: 2-5 minutes

## Individual Targets

Each phase can also be run independently:

```bash
# Just install without dev/test tools
make install

# Quick syntax check only  
make smoke

# Check tools are available (Python, gfortran, cmake)
make health

# Generate HTML coverage report (requires make test first)
make coverage

# Remove venv for clean rebuild
make clean-venv
```

## Verification

After successful `make dev`, verify the extension module loads:

```bash
./.venv/bin/python -c "from pyiri2016 import iriweb; print('✓ Module loaded OK')"
```

## Build Configuration Details

### How It Works

1. **CMake discovers** Python 3.11 in venv and NumPy location
2. **generate_f2py.py** runs f2py to create C wrapper code from Fortran sources
3. **f2py_wrapper.sh** ensures UTF-8 encoding for Fortran source parsing
4. **CMake compiles** the Fortran sources with gfortran
5. **Extension module** (`iriweb.so`) linked against NumPy C API
6. **Package installed** with all data files and Python modules

### UTF-8 Handling

The Fortran source files contain non-ASCII characters that require proper encoding. This is handled by:
- Setting `PYTHONIOENCODING=utf-8` in shell wrappers
- Using `charset-normalizer` for f2py encoding auto-detection
- All build targets export UTF-8 environment variables

## Troubleshooting

### Build fails with CMake errors

**Check CMake version**:
```bash
cmake --version  # Must be 3.15 or newer
```

**Check gfortran**:
```bash
gfortran --version  # Must be available
```

**Clean and retry**:
```bash
make clean-venv
make dev
```

### Module import fails

**Step 1**: Verify Fortran extension compiled
```bash
ls -la .venv/lib/python3.11/site-packages/pyiri2016/iriweb*.so
# Should show the compiled extension module
```

**Step 2**: Check NumPy is available
```bash
./.venv/bin/python -c "import numpy; print(numpy.__version__)"
```

**Step 3**: Check Python path
```bash
./.venv/bin/python -c "import sys; print(sys.path)"
```

### Tests fail to run

**Install test dependencies**:
```bash
./.venv/bin/python -m pip install pytest pytest-cov parameterized
```

**Run with verbose output**:
```bash
./.venv/bin/python -m pytest tests/ -vv --tb=long
```

### Coverage report fails

**Install pytest-cov**:
```bash
./.venv/bin/python -m pip install pytest-cov
```

**Generate coverage**:
```bash
make coverage
# Opens: htmlcov/index.html
```

## Key Files

| File | Purpose |
|------|---------|
| `CMakeLists.txt` | CMake build configuration - edit to change build process |
| `generate_f2py.py` | f2py wrapper - generates C code from Fortran |
| `f2py_wrapper.sh` | Shell wrapper - sets encoding environment variables |
| `pyproject.toml` | PEP 517/518 build config - dependencies and metadata |
| `Makefile` | Build automation - convenient targets |
| `setup.py` | Legacy file - kept for compatibility, not used |


## Next Steps

1. Run `make dev` to complete the installation
2. Run `make test` to verify all tests pass
3. Run `make coverage` to see code coverage report
4. Run `make build` to create distribution packages
5. See `CHANGELOG.md` for release notes

## Success Criteria

After running `make dev && make test`:
- ✅ All 4 tests pass
- ✅ Module imports successfully
- ✅ Fortran extension module (`iriweb.so`) exists
- ✅ Example scripts run and produce correct output


After `make dev`:
```bash
✓ .venv/ directory exists
✓ setuptools==59.6.0 installed
✓ package installed in editable mode
✓ iriweb Fortran extension module compiled
✓ No UTF-8 encoding errors
```

After `make test`:
```bash
✓ All tests discover and run
✓ Coverage report generated
✓ No import errors for iriweb module
```

After `make build`:
```bash
✓ dist/pyiri2016-1.2.0.tar.gz created (source distribution)
✓ dist/pyiri2016-1.2.0-*.whl created (binary wheel)
```

---

**Status**: ✅ All build issues fixed and tested. Ready for production use.
