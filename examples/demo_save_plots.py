#!/usr/bin/env python
"""
Demo script showing how to save plotting examples to files instead of displaying them.
Useful for headless environments, CI/CD pipelines, and batch processing.

Generated plots are saved to figures/ directory.
"""

from pathlib import Path
from pyiri2016 import IRI2016Profile
from pyiri2016.iri2016prof2D import IRI2016_2DProf
from numpy import arange
from matplotlib.pyplot import figure, legend, savefig, close
import seaborn

# Create figures directory
figures_dir = Path(__file__).parent.parent / "figures"
figures_dir.mkdir(exist_ok=True)

print(f"Saving plots to: {figures_dir}\n")

# ============================================================================
# 1D Height Profile Examples
# ============================================================================

print("1. Creating 1D Height Profile (Ne vs Altitude)...")
altlim = [100., 1000.]
altstp = 5.
lat, lon = -11.95, -76.77
year, month, dom = 2003, 11, 21

iri2016Obj = IRI2016Profile(altlim=altlim, altstp=altstp, lat=lat, \
    lon=lon, year=year, month=month, dom=dom, option=1, verbose=False)

altbins = arange(altlim[0], altlim[1] + altstp, altstp)
nalt = len(altbins)
index = range(nalt)

fig = figure(figsize=(16, 6))

pn = fig.add_subplot(121)
ne = iri2016Obj.a[0, index]        
pn.plot(ne, altbins, label='N$_e$')
pn.set_title(iri2016Obj.title1)
pn.set_xlabel('Density (m$^{-3}$)')
pn.set_ylabel('Altitude (km)')
pn.set_xscale('log')
legend(loc='best')

pn = fig.add_subplot(122)
ti = iri2016Obj.a[2, index]
te = iri2016Obj.a[3, index]
pn.plot(ti, altbins, label='T$_i$')
pn.plot(te, altbins, label='T$_e$')
pn.set_title(iri2016Obj.title2)
pn.set_xlabel('Temperature ($^\circ$)')
pn.set_ylabel('Altitude (km)')        
legend(loc='best')

output_file = figures_dir / "1d_height_profile.png"
savefig(str(output_file), bbox_inches='tight', dpi=150)
print(f"   ✓ Saved to {output_file}\n")
close(fig)

# ============================================================================
# 2D Height vs Time Example
# ============================================================================

print("2. Creating 2D Height vs Time profile...")
iri2016Obj_2d = IRI2016_2DProf(altlim=[100., 1000.], altstp=5., hrstp=.25/3, \
    lat=-11.95, lon=-76.77, month=6, option=1, verbose=False)
iri2016Obj_2d.HeightVsTime()
iri2016Obj_2d.Plot2D()

# The Plot2D method calls show() - we need to capture the figure
# Since this is called internally, we'll save the current figure
import matplotlib.pyplot as plt
output_file = figures_dir / "2d_height_vs_time.png"
plt.savefig(str(output_file), bbox_inches='tight', dpi=150)
print(f"   ✓ Saved to {output_file}\n")
close('all')

# ============================================================================
# 2D Latitude vs Longitude Example (with map)
# ============================================================================

print("3. Creating 2D Latitude vs Longitude map profile...")
lonstp = 4
iri2016Obj_latlon = IRI2016_2DProf(hour=17, lat=-11.95, latstp=2., lon=-76.77, \
                                    lonstp=lonstp, month=9, option=2, \
                                    verbose=False, year=2010)
iri2016Obj_latlon.LatVsLon(lonstp=lonstp)
iri2016Obj_latlon.Plot2D()

output_file = figures_dir / "2d_lat_vs_lon_map.png"
plt.savefig(str(output_file), bbox_inches='tight', dpi=150)
print(f"   ✓ Saved to {output_file}\n")
close('all')

print("=" * 70)
print(f"All plots saved successfully to: {figures_dir}")
print("=" * 70)
print("\nTo view the plots:")
print(f"  - Open the PNG files in your image viewer")
print(f"  - Or copy them to your local machine for viewing")
