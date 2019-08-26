
import os
from setuptools import setup, Extension

# enable this option if you want to rebuild the .c file yourself with cython
USE_CYTHON = False

if USE_CYTHON:
    ext = '.pyx'
else:
    ext = '.c'

extensions = [
    Extension(
        "IT8951.spi",
        ["IT8951/spi"+ext],
        libraries=['bcm2835'],
    )
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
    name = "IT8951",
    packages=['IT8951'],
    ext_modules = extensions
)
