"""Packaging logic for GaugeRnR."""
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    packages=['GaugeRnR'],
    install_requires=requirements
)
