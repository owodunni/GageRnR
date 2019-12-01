import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "GaugeRnR",
    version = "0.0.1",
    author = "Alexander Poole",
    author_email = "alex.o.poole@gmail.com",
    description = ("A simple python lib for calculating Gauge RnR."),
    license = "MIT",
    keywords = "statistics gague R&R rnr gagernr",
    url = "http://packages.python.org/GaugeRnR",
    packages=['GaugeRnR', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Beta",
        "Topic :: Statistics",
        "License :: OSI Approved :: MIT License",
    ],
)