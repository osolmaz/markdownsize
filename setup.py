from setuptools import setup, find_packages
from os import path
from setuptools.extension import Extension


here = path.abspath(path.dirname(__file__))


setup(
    name="markdownsize",
    version="0.0",
    description="Write essays in Markdown like writing a Twitter thread",
    author="Onur Solmaz",
    author_email="onur@solmaz.io",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    extras_require={"dev": ["check-manifest"], "test": ["coverage"],},
    entry_points={"console_scripts": ["markdownsize=markdownsize.main:__main__",],},
)
