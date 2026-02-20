# Build Fix Summary - Poetry to UV Migration

## Problem Analysis

The migration from Poetry to UV encountered three distinct issues:

1. **UTF-8 Encoding Error in f2py**: `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2`
2. **setuptools Compatibility**: `TypeError: Compiler.__init__() takes from 1 to 3 positional arguments but 4 were given`
3. **Virtual Environment Initialization**: Missing or stale venv causing build failures

## Solutions Implemented

### 1. UTF-8 Encoding Fix

**What was the problem:**
- Fortran files (especially `irifun.for`) contain non-ASCII characters (smart quotes, special symbols)
- f2py was unable to read these files because PYTHONIOENCODING wasn't being respected in subprocesses

**What was fixed:**
- Added `charset-normalizer>=2.0.0` to build requirements so f2py can auto-detect file encoding
- Set `PYTHONIOENCODING=utf-8` at module level in `setup.py` BEFORE any other imports
- Exported UTF-8 encoding variables globally in `Makefile`

**Files changed:**
- `setup.py`: Added encoding environment setup at top of file (lines 14-28)
- `pyproject.toml`: Added `charset-normalizer>=2.0.0` to build requirements
- `Makefile`: Added global `export PYTHONIOENCODING=utf-8` block
- `setup.py`: Added explicit stdout/stderr UTF-8 wrapper

### 2. setuptools Compatibility with numpy.distutils

**What was the problem:**
- numpy.distutils is deprecated and only compatible with setuptools < 60.0
- Modern setuptools (82.0.0) has changed compiler initialization signature
- Later versions of setuptools removed support for Compiler.__init__() parameter passing

**What was fixed:**
- Explicitly pin setuptools to version 59.6.0 (latest compatible version)
- Specify constraint in both `pyproject.toml` and `Makefile`
- Use `--no-build-isolation` flag to build directly in system environment

**Files changed:**
- `pyproject.toml`: `requires = ["setuptools>=59.6,<60", ...]`
- `Makefile`: All build targets install `setuptools==59.6.0` explicitly

### 3. Virtual Environment Handling

**What was the problem:**
- venv not created before certain operations
- stale or corrupted venv from previous failed builds

**What was fixed:**
- Added `[ -d .venv ] || uv venv` check to dev, build, and install targets
- Ensures fresh venv for each new session

## Configuration Files

### pyproject.toml - Build System
```toml
[build-system]
requires = ["setuptools>=59.6,<60", "numpy>=1.21.5", "charset-normalizer>=2.0.0"]
build-backend = "setuptools.build_meta"
```

### Makefile - Build Targets
```makefile
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

dev:
	[ -d .venv ] || uv venv
	uv pip install --upgrade pip 'setuptools==59.6.0' wheel charset-normalizer
	uv pip install -e . --no-build-isolation
	uv pip install pre-commit coverage parameterized
```

### setup.py - Encoding Initialization
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# CRITICAL: Set encoding environment variables BEFORE any other imports
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['LANG'] = 'en_US.UTF-8'

# Force Python to use UTF-8 for stdin/stdout/stderr
if sys.version_info[0] >= 3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

## Testing the Fix

Run the following commands to verify the migration is working:

```bash
# Development installation with Fortran compilation
make dev

# Verify installation succeeded by importing the extension module
python -c "from pyiri2016 import iriweb; print('✓ Fortran extension compiled successfully')"

# Run full test suite
make test

# Build distribution packages
make build
```

## Expected Output

After a successful `make dev`, you should see:
- Setuptools 59.6.0 being installed
- F2py compiling Fortran files to C (many "rmbadname1" and "append_needs" warnings are normal)
- No UTF-8 decoding errors
- Package installed in editable mode with extension module compiled

## Known Deprecation Warnings

The following warnings are expected and can be safely ignored:
- `numpy.distutils is deprecated since NumPy 1.23.0` - This is acknowledged but required for Python 3.10
- License classifier warnings - These are legacy pyproject.toml warnings
- setuptools deprecation warnings - These are from numpy.distutils, not our code

## Technical Notes

### Why setuptools 59.6.0?
- This is the latest version that works with numpy.distutils
- Later versions changed the Compiler class initialization signature
- Python 3.11+ would allow using `meson` or `scikit-build`, but we're targeting Python 3.9+

### Why --no-build-isolation?
- Allows the build process to access system tools (gfortran)
- Ensures environment variables set in setup.py are respected
- Necessary for numpy.distutils to function with modern setuptools

### Why charset-normalizer?
- Enables f2py to automatically detect file encoding
- f2py's default encoding detection fails on non-UTF-8 Fortran files
- charset-normalizer provides robust file encoding detection

## Troubleshooting

If you still encounter build issues:

1. **Clean the environment**:
   ```bash
   rm -rf .venv build/ dist/ *.egg-info
   make dev
   ```

2. **Check setuptools version**:
   ```bash
   python -m pip show setuptools
   # Should show version 59.6.x
   ```

3. **Verify Fortran compiler**:
   ```bash
   gfortran --version
   ```

4. **Check encoding settings**:
   ```bash
   echo $PYTHONIOENCODING  # Should be utf-8
   ```

## Summary of Changes

| File | Change | Reason |
|------|--------|--------|
| pyproject.toml | Added charset-normalizer to build-requires | f2py encoding detection |
| pyproject.toml | Pinned setuptools to 59.6,<60 | numpy.distutils compatibility |
| setup.py | Encoding setup at module level | Ensure f2py reads UTF-8 files |
| Makefile | Global PYTHONIOENCODING export | Ensure subprocesses inherit encoding |
| Makefile | Explicit setuptools==59.6.0 install | Override UV's version selection |
| Makefile | venv creation check | Prevent stale venv issues |

All changes maintain backward compatibility and don't require modifying Fortran source files or project structure.
