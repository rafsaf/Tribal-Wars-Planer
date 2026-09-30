# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from Cython.Build import cythonize
from setuptools import setup

setup(
    packages=[],
    ext_modules=cythonize(
        [
            "utils/write_noble_target.py",
            "utils/write_ram_target.py",
        ],
        compiler_directives={
            "language_level": "3",
        },
    ),
)
