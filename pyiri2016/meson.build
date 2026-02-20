py = py_mod.find_installation(pure: false)

# Install Python package files
py.install_sources(
  '__init__.py',
  'iri2016prof2D.py',
  subdir: 'pyiri2016',
)

# Install api submodule
install_subdir(
  'api',
  install_dir: py_platlib / 'pyiri2016',
)
