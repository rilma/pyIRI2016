py = py_mod.find_installation(pure: false)

# Fortran sources for the iri2016 module
iri_fortran_sources = [
    'iriwebg.for',
    'irisub.for',
    'irifun.for',
    'iritec.for',
    'iridreg.for',
    'igrf.for',
    'cira.for',
    'iriflip.for',
]

# Create the Python extension module
py.extension_module(
  'iriweb',
  iri_fortran_sources,
  install: true,
  subdir: 'pyiri2016',
)
