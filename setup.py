from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="davat",
    version="0.0.3",
    description="davat(دوات) is a very simple tools for normalizeing and cleaning Persian text",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mh-salari/davat",
    author="MohammadHossein Salari",
    author_email="mohammad.hossein.salari@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(include=["davat", "davat.*"]),
    install_requires=["emoji>=1.2.0"],
)
