#!/usr/bin/env python
from pyiri2016 import IRI2016,IRI2016Profile
from numpy import arange
from matplotlib.pyplot import figure, legend, savefig, close
import seaborn
from pathlib import Path
import uuid

def example02():

    """ Geog. Latitude Profile Example """

    latlim = [-60, 60]
    latstp = 2.
    iri2016Obj = IRI2016Profile(alt=600, hour=17., latlim=latlim, latstp=latstp, \
    lon=-76.77, option=2, verbose=False, year=2004)

    latbins = arange(latlim[0], latlim[1] + latstp, latstp)

    nlat = len(latbins)
    index = range(nlat)

    fig = figure(figsize=(8,12))

    pn = fig.add_subplot(211)        
    NmF2 = iri2016Obj.b[0, index]
    NmF1 = IRI2016()._RmNeg(iri2016Obj.b[2, index])
    NmE = iri2016Obj.b[4, index]        
    pn.plot(latbins, NmF2, label='N$_m$F$_2$')
    pn.plot(latbins, NmF1, label='N$_m$F$_1$')
    pn.plot(latbins, NmE, label='N$_m$E')        
    pn.set_title(iri2016Obj.title1)
    pn.set_xlim(latbins[[0, -1]])
    pn.set_xlabel('Geog. Lat. ($^\circ$)')
    pn.set_ylabel('(m$^{-3}$)')        
    pn.set_yscale('log')
    legend(loc='best')

    pn = fig.add_subplot(212)
    hmF2 = iri2016Obj.b[1, index]
    hmF1 = IRI2016()._RmNeg(iri2016Obj.b[3, index])
    hmE = iri2016Obj.b[5, index]        
    pn.plot(latbins, hmF2, label='h$_m$F$_2$')
    pn.plot(latbins, hmF1, label='h$_m$F$_1$')
    pn.plot(latbins, hmE, label='h$_m$E')        
    pn.set_xlim(latbins[[0, -1]])
    pn.set_title(iri2016Obj.title2)
    pn.set_xlabel('Geog. Lat. ($^\circ$)')
    pn.set_ylabel('(km)')
    legend(loc='best')                

    # Save to figures folder with unique UUID suffix
    output_dir = Path(__file__).parent.parent / "figures"
    output_dir.mkdir(exist_ok=True)
    unique_id = str(uuid.uuid4())[:8]
    output_file = output_dir / f"iri1DExample02_{unique_id}.png"
    savefig(output_file, dpi=100, bbox_inches='tight')
    print(f"✓ Plot saved to: {output_file}")
    close(fig)

if __name__ == '__main__':
    example02()
