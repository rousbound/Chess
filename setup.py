from typing import List

import setuptools


def read_multiline_as_list(file_path: str) -> List[str]:
    with open(file_path) as fh:
        contents = fh.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


requirements = read_multiline_as_list("requirements.txt")

# classifiers = read_multiline_as_list("classifiers.txt")

setuptools.setup(
    name="mychess",
    version="0.0.1",
    author="Geraldo Luiz",
    author_email="geraldorj-2010@hotmail.com",
    description="Chess Game",
    url="",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            # '',
        ],
    },
    python_requires="==3.8",
    install_requires=requirements,
)
