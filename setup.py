
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([
        "src/IT8951/spi.pyx",
        "src/IT8951/img_manip.pyx"
    ])
)
