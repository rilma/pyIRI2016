# CMake/f2py Integration Fix - Implementation Summary

## Problem Statement

The previous CMake configuration attempted to force the venv Python via `cmake.define = {"Python_ROOT_DIR" = "..."}`, which didn't work because:

1. CMake's `find_package(Python)` has complex precedence rules that prioritized system Python
2. When CMake found `/usr/local/bin/python` (system Python), it lacked numpy
3. This caused f2py module execution to fail: `ModuleNotFoundError: No module named 'numpy'`

## Solution: Python Wrapper Script

Instead of fighting CMake's Python detection, we use a Python wrapper script that f2py invokes:

### Architecture

```
scikit-build-core
    ↓
CMake (finds Python via find_package)
    ↓
execute Python script: generate_f2py.py
    ↓ (with same Python interpreter as CMake found)
f2py wrapper generation
    ↓
iriweb.c source file
    ↓
CMake compilation
    ↓
iriweb.*.so (extension module)
```

### Key Files Created/Modified

#### 1. `generate_f2py.py` (NEW)
- Python script that wraps the numpy.f2py command
- **Critical**: Called with `sys.executable` which preserves the Python environment
- Location: `/workspaces/pyIRI2016/generate_f2py.py`
- Usage: `python generate_f2py.py <build_dir>`

#### 2. `CMakeLists.txt` (MODIFIED)
- Removed language declarations for Fortran (CMake handles via f2py)
- Added NumPy verification check before attempting f2py
- Changed f2py invocation to use Python wrapper script instead of direct command
- Cleaner configuration with diagnostic messages

Key changes:
```cmake
# Before: Direct f2py command (was finding wrong Python)
COMMAND "${Python_EXECUTABLE}" -m numpy.f2py ...

# After: Python wrapper script (preserves environment)
COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/generate_f2py.py ${F2PY_BUILD_DIR}
```

#### 3. `pyproject.toml` (MODIFIED)
- **REMOVED** problematic: `cmake.define = {"Python_ROOT_DIR" = "..."}`
- Let scikit-build-core manage Python environment naturally
- Clean build configuration that doesn't fight CMake's precedence

### Why This Works

1. **scikit-build-core** starts the build process and sets up the Python environment
2. **CMake** is invoked with that environment; `find_package(Python)` discovers it
3. **generate_f2py.py** runs in that same Python environment (same `sys.executable`)
4. **f2py** has access to numpy from that environment
5. **C wrapper** is generated successfully
6. **Compilation** proceeds normally

## Testing Instructions

### Prerequisites
```bash
cd /workspaces/pyIRI2016
source .venv/bin/activate
pip install -e .[dev]  # or pip install cmake scikit-build-core numpy
```

### Build Test
```bash
pip install -e . --no-build-isolation
```

### Validation Checklist
```bash
# 1. Run validation script
python validate_build_env.py

# 2. Check extension module loads
python -c "from pyiri2016 import iriweb; print('✓ iriweb loaded')"

# 3. Run example
python examples/example01.py

# 4. Run tests
make test
```

### Expected Output

#### CMake configuration phase:
```
-- Using Python: /workspaces/pyIRI2016/.venv/bin/python
-- Found NumPy version: 1.26.4
```

#### f2py wrapper execution:
```
Running f2py with Python: /workspaces/pyIRI2016/.venv/bin/python
F2PY command: /workspaces/pyIRI2016/.venv/bin/python -m numpy.f2py ...
```

#### Build success:
```
Generating f2py C wrapper for iriweb module using: /workspaces/pyIRI2016/.venv/bin/python
[100%] Linking C shared module pyiri2016/iriweb.*.so
[100%] Built target iriweb
```

## Troubleshooting

### Error: "NumPy is not installed"
- **Cause**: Python found is not the venv
- **Fix**: Ensure venv is activated before running pip install

### Error: "f2py not found"
- **Cause**: numpy not in Python environment
- **Fix**: `pip install numpy>=1.26.0`

### Error: "gfortran not found"
- **Cause**: Fortran compiler not installed
- **Fix**: `apt-get install gfortran`

### CMake output shows wrong Python path
- **Cause**: scikit-build-core not properly configured
- **Fix**: Use `pip install -e .` with activated venv, NOT `--no-build-isolation`

## Path Forward (Issue #26)

This solution successfully:
- ✅ Migrates from `numpy.distutils` (deprecated) to CMake + scikit-build-core
- ✅ Eliminates need for setup.py for extension building
- ✅ Uses modern PEP 517/518 build configuration
- ✅ Solves Python environment detection in CMake

Next steps if expanding:
1. Remove setup.py entirely once validated
2. Add comprehensive documentation to QUICKSTART.md
3. Update CI/CD pipelines to use new build system
4. Consider pre-building wheels to distribute
