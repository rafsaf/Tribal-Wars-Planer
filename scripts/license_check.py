import pathlib
from textwrap import dedent

working_dir = pathlib.Path(__file__).parent.parent.absolute()
license_short_text = dedent(
    """
    # Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #     http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
    # ==============================================================================
"""
)


def find_python_files(path: pathlib.Path) -> list[pathlib.Path]:
    python_file_lst: list[pathlib.Path] = []
    for root, dirs, files in path.walk():
        for file in files:
            if file.endswith(".py"):
                python_file_lst.append(root / file)
        for dir in dirs:
            python_file_lst += find_python_files(root / dir)
    return python_file_lst


for python_file in find_python_files(working_dir):
    if "Rafał Safin (rafsaf). All Rights Reserved." in python_file.read_text():
        continue
    print(f"---> {python_file}")
    current_file_text = python_file.read_text()
    with open(python_file, "w") as file_to_update:
        file_to_update.write(license_short_text.strip() + "\n\n" + current_file_text)
