#!/usr/bin/env python
from pyiri2016.iri2016prof2D import IRI2016_2DProf


def example02():
    print("\n=== IRI2016 2D Example 02: Latitude vs Longitude ===")
    print("Parameters: hour 17 UT, latitude -11.95°, longitude -76.77°, September 2010")
    print("Computing 2D profile...")

    lonstp = 4

    iri2016Obj = IRI2016_2DProf(
        hour=17,
        lat=-11.95,
        latstp=2.0,
        lon=-76.77,
        lonstp=lonstp,
        month=9,
        option=2,
        verbose=False,
        year=2010,
    )
    iri2016Obj.LatVsLon(lonstp=lonstp)
    print("Generating plot...")
    iri2016Obj.Plot2D()
    print("Done!")


if __name__ == "__main__":
    # 2D Example: Lat vs Lon, Earth's Map
    example02()
