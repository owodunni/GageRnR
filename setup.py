from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name = "GaugeRnR",
    version = "0.1.0",
    author = "Alexander Poole",
    author_email = "alex.o.poole@gmail.com",
    description = ("A simple python lib for calculating Gauge RnR."),
    license = license,
    keywords = "statistics gague R&R rnr gagernr",
    url = "https://github.com/owodunni/GaugeRnR",
    packages=['GaugeRnR'],
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Beta",
        "Topic :: Statistics",
        "License :: OSI Approved :: MIT License",
    ],
)