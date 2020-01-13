"""Top-level module for GageRnR.

This module
- contains Gauge RnR logic
"""
from .gageRnR import GageRnR
from .generator import Distribution, Settings, Generator
from .__main__ import main
from .dataLoader import DataLoader
from .statistics import Statistics, Result, Component
from .normality import Normality
from .linearity import Linearity

__all__ = ['GageRnR',
           'Component',
           'Result',
           'Distribution',
           'Settings',
           'Generator',
           'main',
           'DataLoader',
           'Statistics',
           'Normality',
           'Linearity', ]

__version__ = "0.6.4"
__version_info__ = tuple(
    int(i) for i in __version__.split(".") if i.isdigit()
)
