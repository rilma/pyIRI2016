#!/usr/bin/env python3
"""
Wrapper script to generate f2py module using the current Python interpreter.
This ensures f2py uses the same Python environment (with numpy) that called this script.
"""
import sys
import os
import subprocess
import shutil
from pathlib import Path
import numpy.f2py

# CRITICAL: Set encoding environment variables BEFORE any other imports
# This ensures f2py and all subprocesses handle UTF-8 correctly
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['LANG'] = 'en_US.UTF-8'

def main():
    """Generate f2py wrapper for iriweb module."""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    source_dir = script_dir / "source"
    build_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    # Fortran source files
    fortran_sources = [
        "iriwebg.for",
        "irisub.for", 
        "irifun.for",
        "iritec.for",
        "iridreg.for",
        "igrf.for",
        "cira.for",
        "iriflip.for"
    ]
    
    source_files = [str(source_dir / f) for f in fortran_sources]
    
    # f2py command - expose all needed subroutines
    # This tells f2py to wrap iriwebg, iritec, irisubgl, and firisubl
    cmd = [
        sys.executable,
        "-m", "numpy.f2py",
        "-m", "iriweb",
        "--build-dir", str(build_dir),
        "--quiet",
        "only:", "iriwebg", "iritec", "irisubgl", "firisubl", ":"
    ] + source_files
    
    print(f"Running f2py with Python: {sys.executable}")
    print(f"F2PY command: {' '.join(cmd)}")
    
    # Pass environment with explicit UTF-8 encoding set to subprocess
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANG'] = 'en_US.UTF-8'
    
    result = subprocess.run(cmd, cwd=str(source_dir), env=env)
    
    if result.returncode != 0:
        print(f"Error: f2py wrapper generation failed with return code {result.returncode}", file=sys.stderr)
        print(f"Build directory: {build_dir}", file=sys.stderr)
        print("Checking if files exist in build directory...", file=sys.stderr)
        for f in Path(build_dir).glob("*"):
            print(f"  {f.name}", file=sys.stderr)
        return result.returncode
    
    # Copy numpy f2py support files to build directory if they're needed but missing
    f2py_dir = Path(numpy.f2py.__file__).parent
    fortranobject_h = f2py_dir / "src" / "fortranobject.h"
    fortranobject_c = f2py_dir / "src" / "fortranobject.c"
    
    build_dir_path = Path(build_dir)
    
    if fortranobject_h.exists():
        shutil.copy(fortranobject_h, build_dir_path / "fortranobject.h")
        print(f"Copied fortranobject.h to {build_dir_path}")
    
    if fortranobject_c.exists():
        shutil.copy(fortranobject_c, build_dir_path / "fortranobject.c")
        print(f"Copied fortranobject.c to {build_dir_path}")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
