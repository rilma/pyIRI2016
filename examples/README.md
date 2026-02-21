# Plotting Examples

This directory contains example scripts demonstrating IRI2016 ionospheric profile calculations and visualizations.

## Running Examples

### Basic Examples (No Plotting Dependencies Required)
```bash
python examples/example01.py
python examples/example02.py
```

### Plotting Examples (Requires `plotting` extras)

Install plotting dependencies:
```bash
make dev-plotting
```

**Interactive Display (requires X11/display):**
```bash
# 1D Height Profiles
python examples/iri1DExample01.py
python examples/iri1DExample01b.py
python examples/iri1DExample02.py
python examples/iri1DExample08.py
```

**Headless Rendering with File Output:**
```bash
# Generate plots and save to figures/ directory
make demo-plots

# Or manually with MPLBACKEND=Agg
MPLBACKEND=Agg python examples/demo_save_plots.py
```

### 2D Map Examples

Located in `scripts/` directory:
```bash
# Headless rendering (saves plots)
MPLBACKEND=Agg python scripts/iri2DExample01.py
MPLBACKEND=Agg python scripts/iri2DExample02.py
```

## demo_save_plots.py

This script demonstrates how to save plotting examples to PNG files instead of displaying them interactively. This is useful for:

- **Headless environments** (CI/CD, Docker containers, remote servers)
- **Batch processing** (generating multiple plots automatically)
- **Documentation** (creating static plot galleries)
- **Non-interactive workflows**

All plots are saved to the `figures/` directory as high-quality PNG files (150 DPI).

## Output Locations

- **Interactive plots**: Displayed in matplotlib window
- **Saved plots**: `figures/` directory relative to project root
  - `1d_height_profile.png` - Height vs. electron density and temperature
  - `2d_height_vs_time.png` - 2D profile height vs. time
  - `2d_lat_vs_lon_map.png` - 2D latitude vs. longitude map with Basemap

## Testing Examples

Run all examples (including headless plotting):
```bash
make test-examples
```

## Notes

- Some advanced methods (`LatVsFL`, IGRF calculations) require additional optional dependencies
- Use `MPLBACKEND=Agg` for headless plotting (no X11 display required)
- Modify example scripts to customize parameters (latitude, longitude, altitude range, etc.)
