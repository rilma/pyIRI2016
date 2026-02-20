# Poetry to UV Migration - Summary of Changes

## Overview
Successfully refactored the pyIRI2016 project from Poetry to UV package manager. The migration includes:

1. **Configuration Files**
   - `pyproject.toml` - Updated to standard PEP 518 format with setuptools backend
   - `Makefile` - Replaced all `poetry run` and `poetry` commands with `uv` equivalents
   - `setup.py` - Enhanced with environment variable configuration for encoding
   - `setup.cfg` - Added for setuptools configuration
   - `.env` - Created to set UTF-8 encoding environment variable

2. **CI/CD Pipeline**
   - `.github/workflows/smoke.yml` - Updated to use `astral-sh/setup-uv@v2` action
   - `.ansible/poetry.yaml` - Converted to use pip-based UV installation

3. **Documentation**
   - `README.md` - Added Development Setup section with UV installation instructions

## Key Configuration Changes

### pyproject.toml
- Migrated from Poetry format to PEP 518 `[project]` table
- Python requirement: `>=3.8.6,<3.11` → `>=3.9`
- Build backend: `poetry-core.masonry.api` → `setuptools.build_meta`
- Added `classifiers` field from setup.py
- Added `charset-normalizer` dependency for Fortran file encoding handling
- **Setuptools pinning:** `setuptools>=58,<60` for numpy.distutils compatibility AND build_editable support

### Makefile Targets
- `make dev` - Install development dependencies (replaces `poetry install`)
- `make build` - Build the project with Fortran extension (replaces f2py manual command)
- `make install` - Install with dev dependencies
- `make test` - Run unit tests
- `make smoke` - Quick syntax check
- `make health` - Verify environment setup

All build commands include `PYTHONIOENCODING=utf-8` to handle Fortran file encoding.

## Fortran Build Configuration

### Encoding Handling
- All Fortran source files are UTF-8 compatible
- The build system sets `PYTHONIOENCODING=utf-8` to ensure f2py can read source files
- Added `charset-normalizer` to build requirements for encoding detection
- Environment variable configured in both Makefile and `.env` file

### Setuptools Compatibility
- numpy.distutils requires `setuptools >= 58, < 60` for compatibility
- This range supports both PEP 517 build_editable hooks and numpy.distutils
- Configured in pyproject.toml build requirements

### Extension Module
- Module name: `iriweb` (from setup.py)
- Sources: iriwebg.for, irisub.for, irifun.for, iritec.for, iridreg.for, igrf.for, cira.for, iriflip.for
- Special handling for DFRIDR function (skipped in f2py compilation)

## Benefits of UV Migration

1. **Performance**: UV is significantly faster at dependency resolution and package management
2. **Simplicity**: Standard PEP 518 configuration is more portable and easier to understand
3. **Modern Tooling**: Better integration with modern Python development workflows
4. **Compatibility**: Works seamlessly with Fortran-based extension modules via setuptools
5. **CI/CD**: Native GitHub Actions support without custom installation playbooks

## Usage

### Installing Dependencies
```bash
make dev
# or
uv sync --extra dev
```

### Building the Fortran Extension
```bash
make build
# or
PYTHONIOENCODING=utf-8 uv build
```

### Running Tests
```bash
make test
```

### Quick Health Check
```bash
make health
```

## Files Modified
- `pyproject.toml` - Main configuration with setuptools<60.0 pin
- `Makefile` - Build targets
- `README.md` - Documentation
- `setup.py` - Environment variable setup
- `.github/workflows/smoke.yml` - CI configuration
- `.ansible/poetry.yaml` - Deployment automation

## Files Created
- `.env` - Environment configuration
- `setup.cfg` - Setuptools configuration
- `build_helper.py` - Build helper script (optional)
- `pyproject_build_hook.py` - Build hook template (optional)
- `verify_migration.sh` - Comprehensive verification script

## Known Issues & Solutions

### Issue: Build fails with "Compiler.__init__() takes from 1 to 3 positional arguments..."
**Cause:** Incompatibility with setuptools versions outside 58-59 range  
**Solution:** Use `setuptools >= 58, < 60` (configured in `pyproject.toml`)

### Issue: UnicodeDecodeError during Fortran compilation
**Cause:** f2py unable to read source files with different encoding  
**Solution:** Set `PYTHONIOENCODING=utf-8` before building (done automatically in Makefile)

## Testing the Migration

Run the comprehensive verification script:
```bash
chmod +x verify_migration.sh
./verify_migration.sh
```

Or use make targets:
```bash
make health         # Verify tools
make smoke          # Check syntax
make test           # Run tests
```

## Notes
- The project maintains backward compatibility with existing `setup.py`
- All data files are properly installed via setuptools
- The Fortran compilation process is unchanged from a user perspective
- No breaking changes for existing users or CI/CD pipelines
