[![Build Status](https://travis-ci.org/rilma/pyIRI2016.svg?branch=master)](https://travis-ci.org/rilma/pyIRI2016)
[![alt tag](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)

# pyIRI2016

![alt tag](figures/iri2DExample02.gif)

A Python interface to the [International Reference Ionosphere (IRI) 2016 model](http://irimodel.org/). 


## Installing

    pip install pyiri2016

Or
```sh
pip install -e .
```
This also installs [Time Utilities](https://github.com/rilma/TimeUtilities).

## Test

```sh
make test
```

## Examples

### Height-profile
Use this [script](examples/iri1DExample01.py) to generate a plot of density and temperatures vs height:

![alt tag](figures/iri1DExample01.png)

### Latitudinal profile
Use this [script](examples/iri1DExample02.py) to generate a plot of densities and height at the peak of F2, F2, and E regions vs geographic latitude:

![alt tag](figures/iri1DExample02.png)

### GMT profile
Use this [script](examples/iri1DExample08.py) to generate a plot of densities and height at the peak of F2, F2, and E regions vs universal time:

![alt tag](figures/iri1DExample08.png)

### Height vs GMT
Use this [script](scripts/iri2DExample01.py) to generate a plot of Ne, Te, and Ti as a function of height and universal time:

![alt tag](figures/iri2DExample01.png)

### Latitude vs Longitude
Use this [script](scripts/iri2DExample02.py) to generate a plot of foF2 a function of geographic latitude and longitude:

![alt tag](figures/iri2DExample02.png)

## Reference
These commands are not normally needed unless you want to work with the Fortran code more directly.

### Compile IRI2016 Fortran

#### In Docker
[Python dev container](https://github.com/microsoft/vscode-remote-try-python) provides a way to isolate runtime stack and its prerequisites. In Visual Studio Code, open a folder in the development container as described [here](https://code.visualstudio.com/docs/remote/containers-tutorial). In a terminal session, pyIRI2016 can be build up as follows:

```sh
make build
```

#### Deprecated

```sh
cd bin
cmake ../source
make
./testiri2016
```

### Manual f2py compile
The function `DFRIDR()` inside `igrf.for` dynamically calls other functions. 
This is something `f2py` can't access directly, so we tell `f2py` not to hook into function `DFRIDF()` with the end statement `skip: dfridr`
```sh
f2py -m iri2016 -c iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for  cira.for iriflip.for  skip: dfridr
```

### manual f2py: IGRF only
```sh
f2py -m igrf -c irifun.for igrf.for skip: dfridr
```
