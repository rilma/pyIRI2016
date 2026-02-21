cmake_minimum_required(VERSION 3.15)
project(pyiri2016 LANGUAGES C Fortran)

# scikit-build-core will set Python_EXECUTABLE to the correct Python
# If not set, use the current Python
find_package(Python 3.11 EXACT COMPONENTS Interpreter Development.Module REQUIRED)

message(STATUS "Using Python: ${Python_EXECUTABLE}")
message(STATUS "Python version: ${Python_VERSION}")

# Verify NumPy is available in the Python environment
execute_process(
  COMMAND ${Python_EXECUTABLE} -c "import numpy; print(numpy.__version__)"
  RESULT_VARIABLE NUMPY_CHECK
  OUTPUT_VARIABLE NUMPY_VERSION
  OUTPUT_STRIP_TRAILING_WHITESPACE
  ERROR_QUIET
)

if(NOT NUMPY_CHECK EQUAL "0")
  message(FATAL_ERROR "NumPy is not installed in the Python environment at ${Python_EXECUTABLE}. This is required to build the f2py extension module.")
endif()

message(STATUS "Found NumPy version: ${NUMPY_VERSION}")

# Fortran source files for iriweb extension
set(FORTRAN_SOURCES
    source/iriwebg.for
    source/irisub.for
    source/irifun.for
    source/iritec.for
    source/iridreg.for
    source/igrf.for
    source/cira.for
    source/iriflip.for
)

# Output directory for f2py-generated C wrapper
set(F2PY_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/f2py_build")
file(MAKE_DIRECTORY "${F2PY_BUILD_DIR}")

# Run shell wrapper script to generate f2py wrapper
# The wrapper ensures UTF-8 environment variables are set correctly
add_custom_command(
  OUTPUT 
    ${F2PY_BUILD_DIR}/iriwebmodule.c 
    ${F2PY_BUILD_DIR}/iriweb-f2pywrappers.f 
    ${F2PY_BUILD_DIR}/fortranobject.h
    ${F2PY_BUILD_DIR}/fortranobject.c
  COMMAND ${CMAKE_COMMAND} -E env PYTHON_EXECUTABLE=${Python_EXECUTABLE} bash ${CMAKE_CURRENT_SOURCE_DIR}/f2py_wrapper.sh ${F2PY_BUILD_DIR}
  DEPENDS ${FORTRAN_SOURCES} ${CMAKE_CURRENT_SOURCE_DIR}/generate_f2py.py ${CMAKE_CURRENT_SOURCE_DIR}/f2py_wrapper.sh
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMENT "Generating f2py C wrapper for iriweb module"
  VERBATIM
)

# Create the extension module from f2py-generated wrapper and Fortran sources
Python_add_library(iriweb MODULE
  ${F2PY_BUILD_DIR}/iriwebmodule.c
  ${F2PY_BUILD_DIR}/iriweb-f2pywrappers.f
  ${F2PY_BUILD_DIR}/fortranobject.c
  ${FORTRAN_SOURCES}
)

# Suppress Fortran compiler warnings
target_compile_options(iriweb PRIVATE -w)

# Get NumPy include directory and f2py support
execute_process(
  COMMAND ${Python_EXECUTABLE} -c "import numpy; print(numpy.get_include())"
  RESULT_VARIABLE NUMPY_INCLUDE_RESULT
  OUTPUT_VARIABLE NUMPY_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

if(NOT NUMPY_INCLUDE_RESULT EQUAL "0")
  message(FATAL_ERROR "Failed to determine NumPy include directory")
endif()

# Get f2py fortranobject include directory
execute_process(
  COMMAND ${Python_EXECUTABLE} -c "import numpy.f2py; import os; print(os.path.dirname(numpy.f2py.__file__))"
  RESULT_VARIABLE F2PY_DIR_RESULT
  OUTPUT_VARIABLE F2PY_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(STATUS "NumPy include directory: ${NUMPY_INCLUDE_DIR}")
message(STATUS "f2py directory: ${F2PY_DIR}")

# Include directories for the module
target_include_directories(iriweb PRIVATE 
  ${Python_INCLUDE_DIRS}
  ${NUMPY_INCLUDE_DIR}
  ${F2PY_DIR}
  ${F2PY_BUILD_DIR}
)

# Link Python libraries
target_link_libraries(iriweb PRIVATE ${Python_LIBRARIES})

# Set output directory for extension module (expected by scikit-build-core)
set_target_properties(iriweb PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/pyiri2016"
)

# Install the extension module
install(TARGETS iriweb DESTINATION pyiri2016 COMPONENT python)

# Install data files
set(DATA_DIRS
    data/ccir
    data/igrf
    data/index
    data/mcsat
    data/ursi
)

foreach(DATA_DIR ${DATA_DIRS})
  file(GLOB DATA_FILES "${CMAKE_CURRENT_SOURCE_DIR}/${DATA_DIR}/*")
  if(DATA_FILES)
    install(FILES ${DATA_FILES} DESTINATION pyiri2016/${DATA_DIR} COMPONENT python)
  endif()
endforeach()
