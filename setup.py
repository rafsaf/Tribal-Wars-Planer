from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize(
        [
            "utils/write_noble_target.py",
            "utils/outline_complete.py",
            "utils/write_ram_target.py",
            "utils/fast_weight_maximum.py",
            "utils/basic/ruin.py",
        ],
        compiler_directives={"language_level": "3"},
    )
)
