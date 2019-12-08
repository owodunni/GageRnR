"""Top-level module for GaugeRnR.

This module
- contains Gauge RnR logic
"""
from .gaugeRnR import GaugeRnR, Component, Result
from .generator import Distribution, Settings, Generator
from .__main__ import main
from .dataLoader import DataLoader

__all__ = ['GaugeRnR',
           'Component',
           'Result',
           'Distribution',
           'Settings',
           'Generator',
           'main',
           'DataLoader', ]

__version__ = "0.2.0"
__version_info__ = tuple(
    int(i) for i in __version__.split(".") if i.isdigit()
)
