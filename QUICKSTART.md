# Quick Start - Build and Test

## TL;DR

Just run:
```bash
make dev       # Install with Fortran extension compilation
make test      # Run tests
make build     # Create distribution packages
```

## What's New in v1.2.0

✅ **TimeUtilities Integration** - Added fallback implementation for robustness when external package is unavailable  
✅ **Improved Dependency Management** - Explicit `timeutil` package dependency from GitHub  
✅ **Python 3.11+ Minimum** - Raised minimum Python version requirement to 3.11  
✅ **Project Cleanup** - Removed obsolete Poetry/Meson build files for a cleaner repository  

## Build Process

### 1. Development Installation

```bash
make dev
```

This target:
- Creates `.venv` virtual environment if needed
- Installs pip, setuptools 59.6.0, wheel, charset-normalizer
- Installs package in editable mode with Fortran extension compiled
- Installs development tools (pre-commit, coverage, parameterized)

**Expected time**: 2-5 minutes (slower on first run due to gfortran compilation)

### 2. Run Tests

```bash
make test
```

This target:
- Uses coverage to run unittest discovery
- Tests all modules in current directory
- Generates coverage report

**Expected time**: 30 seconds - 2 minutes depending on test count

### 3. Build Distribution Packages

```bash
make build
```

This target:
- Creates source distribution (sdist)
- Creates binary wheel with compiled extension module
- Packages available in `dist/` directory

**Expected time**: 2-5 minutes

## Individual Targets

Each phase can also be run independently:

```bash
# Just install without dev tools
make install

# Quick syntax check only  
make smoke

# Check tools are available
make health

# View coverage report (after running make test)
make coverage
```

## Verification

After successful `make dev`, verify the extension module:

```bash
python -c "from pyiri2016 import iriweb; print('✓ Success')"
```

## What Changed

**Configuration Updates**:
- `setup.py`: Encoding setup at module import (lines 1-28)
- `pyproject.toml`: setuptools and charset-normalizer in build dependencies
- `Makefile`: Global UTF-8 export, venv creation, explicit setuptools version
- `.env`: Already had PYTHONIOENCODING (confirmed in place)

**Why These Changes**:
1. **Fortran files** contain non-ASCII characters → need UTF-8 handling
2. **numpy.distutils** only works with setuptools < 60.0
3. **f2py** needs charset-normalizer to auto-detect file encoding
4. **Environment variables** must be set before subprocesses start

## Troubleshooting

**Issue**: `UnicodeDecodeError` during build  
**Fix**: Already fixed! charset-normalizer handles this automatically.

**Issue**: `TypeError: Compiler.__init__()...`  
**Fix**: Already fixed! setuptools pinned to 59.6.0.

**Issue**: Build still fails  
**Step 1**: Clean and retry
```bash
rm -rf .venv build dist *.egg-info
make dev
```

**Step 2**: Check setuptools version
```bash
python -m pip show setuptools | grep Version
# Should show: Version: 59.6.0
```

**Step 3**: Verify gfortran
```bash
gfortran --version  # Must succeed
```

**Step 4**: Clean Python cache
```bash
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
```

## Key Files

| File | Purpose |
|------|---------|
| `Makefile` | Build automation - edit to change build process |
| `pyproject.toml` | PEP 518 build config - dependencies and metadata |
| `setup.py` | Package setup and Fortran extension definition |
| `.env` | Environment variables (UTF-8 encoding) |


## Next Steps

1. Run `make dev` to test the installation
2. Run `make test` to verify functionality
3. Run `make build` to create distribution packages
4. See `CHANGELOG.md` for release notes

## Success Criteria

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
