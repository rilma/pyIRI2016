#!/usr/bin/env python
"""
Build helper to fix Fortran file encoding issues for f2py
"""
import os
import sys
from pathlib import Path

def fix_fortran_encoding():
    """Convert Fortran files to ASCII-safe encoding."""
    source_dir = Path('source')
    fortran_files = list(source_dir.glob('*.for'))
    
    errors_found = False
    for fort_file in fortran_files:
        try:
            # Try reading with UTF-8, if it fails, we have encoding issues
            with open(fort_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✓ {fort_file.name} - UTF-8 compatible")
        except UnicodeDecodeError as e:
            print(f"✗ {fort_file.name} - Encoding issue detected")
            errors_found = True
            
            # Try with latin-1 and convert to ASCII
            try:
                with open(fort_file, 'r', encoding='latin-1') as f:
                    content = f.read()
                
                # Replace common non-ASCII characters
                content = content.replace('°', 'o')  # degree symbol
                content = content.replace('±', '+/-')
                content = content.replace('×', '*')
                content = content.replace('÷', '/')
                content = content.replace('α', 'alpha')
                content = content.replace('β', 'beta')
                content = content.replace('γ', 'gamma')
                content = content.replace('δ', 'delta')
                content = content.replace('ε', 'epsilon')
                content = content.replace('π', 'pi')
                
                with open(fort_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Fixed {fort_file.name}")
            except Exception as fix_error:
                print(f"  Failed to fix: {fix_error}")

if __name__ == '__main__':
    # Set encoding environment variable
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    os.environ['LANG'] = 'en_US.UTF-8'
    
    fix_fortran_encoding()
