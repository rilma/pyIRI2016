#!/bin/bash
set -e
cd /workspaces/pyIRI2016
source .venv/bin/activate
python -m pip install -e . --no-build-isolation 2>&1 | tee build.log
echo "Build completed with exit code: $?"
