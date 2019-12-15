"""Top-level module for GaugeRnR.

This module
- contains Gauge RnR logic
"""
from .gaugeRnR import GaugeRnR
from .generator import Distribution, Settings, Generator
from .__main__ import main
from .dataLoader import DataLoader
from .statistics import Statistics, Result, Component
from .normality import Normality
from .linearity import Linearity

__all__ = ['GaugeRnR',
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

__version__ = "0.5.0"
__version_info__ = tuple(
    int(i) for i in __version__.split(".") if i.isdigit()
)
