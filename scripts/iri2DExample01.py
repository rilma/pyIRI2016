#!/usr/bin/env python
from pyiri2016.iri2016prof2D import IRI2016_2DProf


def example01():
    print("\n=== IRI2016 2D Example 01: Height vs Time ===")
    print("Parameters: altitude 100-1000 km, latitude -11.95°, longitude -76.77°, June")
    print("Computing 2D profile...")

    iri2016Obj = IRI2016_2DProf(
        altlim=[100.0, 1000.0],
        altstp=5.0,
        hrstp=0.25 / 3,
        lat=-11.95,
        lon=-76.77,
        month=6,
        option=1,
        verbose=False,
    )
    iri2016Obj.HeightVsTime()
    print("Generating plot...")
    iri2016Obj.Plot2D()
    print("Done!")


if __name__ == "__main__":
    # 2D Example: Height vs Time
    example01()
