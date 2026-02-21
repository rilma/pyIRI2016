#!/bin/bash
# Wrapper script to ensure f2py generation handles UTF-8 encoding correctly

export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Get the Python executable from environment or use system python3
PYTHON_EXE="${PYTHON_EXECUTABLE:-python3}"

# Run the Python wrapper script
"$PYTHON_EXE" /workspaces/pyIRI2016/generate_f2py.py "$@"
