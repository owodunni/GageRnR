"""Packaging logic for GageRnR."""
from setuptools import setup, find_packages

with open('pip/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    packages=find_packages(),
    package_data={'': ['*.css']},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'GageRnR = GageRnR.__main__:main'
        ]
    })
