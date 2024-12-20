"""Install parameters for CLI and python import."""
from setuptools import find_packages, setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name="campbell",
    version="0.0.1",
    description="Python package for campbell scientific data loggers.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/treychaffin/campbell",
    author="Trey Chaffin",
    author_email="treychaffin@gmail.com",
    maintainer="Trey Chaffin",
    maintainer_email="treychaffin@gmail.com",
    package_data={"campbell": ["py.typed"]},
    install_requires=["requests >= 2.32.3"],
    python_requires=">=3.12",
    license="GPLv2",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
    ],
)
