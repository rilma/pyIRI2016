# Examples

This directory contains example scripts demonstrating IRI2016 ionospheric profile calculations.

## Running Examples

### Basic Examples
```bash
python examples/example01.py
python examples/example02.py
```

### 1D Profile Examples (Height, Latitude, Time)

First, install plotting dependencies:
```bash
make dev-plotting
```

Then run the examples:
```bash
python examples/iri1DExample01.py   # Height profile
python examples/iri1DExample01b.py  # Height profile (alternate)
python examples/iri1DExample02.py   # Latitude profile
python examples/iri1DExample08.py   # Time profile
```

### 2D Examples

First, install plotting dependencies:
```bash
make dev-plotting
```

Then run the 2D examples (located in `scripts/` directory):
```bash
python scripts/iri2DExample01.py    # Height vs. Time
python scripts/iri2DExample02.py    # Latitude vs. Longitude
```

## Notes

- For headless environments, use: `MPLBACKEND=Agg python examples/iri1DExample01.py`
- Modify example scripts to customize parameters (latitude, longitude, altitude range, etc.)

