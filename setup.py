"""Packaging logic for GaugeRnR."""
from setuptools import setup

with open('pip/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    packages=['GaugeRnR'],
    install_requires=requirements,
    entry_points = {
        'console_scripts': [
            'GaugeRnR = GaugeRnR.__main__:main'
        ]
    })
