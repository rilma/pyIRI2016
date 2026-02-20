"""
Hook for setuptools to handle Fortran file encoding before building.
Place this in the build hook directory.
"""
import os
import sys
from pathlib import Path

def hook_setup(*args, **kwargs):
    """Pre-build hook to fix encoding issues."""
    # Ensure UTF-8 encoding
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    
    source_dir = Path('source')
    for fort_file in source_dir.glob('*.for'):
        try:
            # Try UTF-8 first
            with open(fort_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fall back to latin-1 and save as UTF-8
            with open(fort_file, 'r', encoding='latin-1') as f:
                content = f.read()
            
            with open(fort_file, 'w', encoding='utf-8') as f:
                f.write(content)
