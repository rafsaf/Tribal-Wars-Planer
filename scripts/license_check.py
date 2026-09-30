import pathlib
from textwrap import dedent

working_dir = pathlib.Path(__file__).parent.parent.absolute()
license_short_text = dedent(
    """
    # Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
    # GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)
"""
)


def find_python_files(path: pathlib.Path) -> list[pathlib.Path]:
    python_file_lst: list[pathlib.Path] = []
    for root, dirs, files in path.walk():
        # Remove unwanted directories to prevent walk from descending into them
        dirs[:] = [d for d in dirs if d not in {".venv", "venv", "__pycache__"}]

        for file in files:
            if file.endswith(".py"):
                file_path = root / file
                if file == "__init__.py" and not file_path.read_text().strip():
                    continue
                python_file_lst.append(file_path)
    return python_file_lst


for python_file in find_python_files(working_dir):
    if "Rafał Safin (rafsaf). All Rights Reserved." in python_file.read_text():
        continue
    print(f"---> {python_file}")
    current_file_text = python_file.read_text()
    with open(python_file, "w") as file_to_update:
        file_to_update.write(license_short_text.strip() + "\n\n" + current_file_text)
