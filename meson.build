project(
  'pyiri2016',
  'fortran',
  version: '1.2.2',
  meson_version: '>=1.0.0',
)

py_mod = import('python')
py = py_mod.find_installation(pure: false)

py_purelib = py.get_install_dir(
  subdir: 'pure',
)

py_platlib = py.get_install_dir(
  subdir: 'platlib',
)

# Build the Fortran extension module
subdir('source')

# Install data files
install_subdir(
  'pyiri2016/data',
  install_dir: py_platlib / 'pyiri2016',
)

# Install Python modules
subdir('pyiri2016')
