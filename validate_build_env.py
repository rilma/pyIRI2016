#!/usr/bin/env python3
"""
Validation script to check if the build environment is properly configured.
"""
import sys
import subprocess
from pathlib import Path

def check_cmake():
    """Check if CMake is available and correct version."""
    try:
        result = subprocess.run(["cmake", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ cmake found")
            print(f"  {result.stdout.split(chr(10))[0]}")
            return True
    except FileNotFoundError:
        print("✗ cmake not found")
    return False

def check_python():
    """Check Python executable and environment."""
    print(f"✓ Python: {sys.executable}")
    print(f"  Version: {sys.version}")
    return True

def check_numpy():
    """Check numpy availability."""
    try:
        import numpy
        print(f"✓ NumPy: {numpy.__version__}")
        return True
    except ImportError:
        print("✗ NumPy not found")
        return False

def check_scikit_build_core():
    """Check scikit-build-core availability."""
    try:
        import scikit_build_core
        print(f"✓ scikit-build-core available")
        return True
    except ImportError:
        print("✗ scikit-build-core not found")
        return False

def check_fortran_compiler():
    """Check Fortran compiler availability."""
    try:
        result = subprocess.run(["gfortran", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ gfortran found")
            return True
    except FileNotFoundError:
        print("✗ gfortran not found")
    return False

def check_f2py():
    """Check f2py availability."""
    try:
        result = subprocess.run([sys.executable, "-m", "numpy.f2py", "--version"], capture_output=True, text=True)
        if result.returncode == 0 or "numpy.f2py" in result.stderr:
            print(f"✓ f2py available")
            return True
    except Exception:
        pass
    print("✗ f2py not available")
    return False

def check_source_files():
    """Check if Fortran source files exist."""
    source_dir = Path(__file__).parent / "source"
    fortran_files = [
        "iriwebg.for",
        "irisub.for", 
        "irifun.for",
        "iritec.for",
        "iridreg.for",
        "igrf.for",
        "cira.for",
        "iriflip.for"
    ]
    
    all_exist = True
    for f in fortran_files:
        path = source_dir / f
        if path.exists():
            print(f"✓ {f}")
        else:
            print(f"✗ {f} not found")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks."""
    print("=" * 60)
    print("Build Environment Validation")
    print("=" * 60)
    
    print("\n[CMake]")
    cmake_ok = check_cmake()
    
    print("\n[Python]")
    python_ok = check_python()
    
    print("\n[Required Packages]")
    numpy_ok = check_numpy()
    sbc_ok = check_scikit_build_core()
    
    print("\n[Compilers]")
    gfortran_ok = check_fortran_compiler()
    f2py_ok = check_f2py()
    
    print("\n[Fortran Sources]")
    sources_ok = check_source_files()
    
    print("\n" + "=" * 60)
    if all([cmake_ok, python_ok, numpy_ok, sbc_ok, gfortran_ok, f2py_ok, sources_ok]):
        print("✓ All checks passed! Ready to build.")
        return 0
    else:
        print("✗ Some checks failed. See above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
