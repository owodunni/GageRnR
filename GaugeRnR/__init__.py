"""Top-level module for GaugeRnR.

This module
- contains Gauge RnR logic
"""
from .gaugeRnR import GaugeRnR, Component, Result
from .generator import Distribution, Settings, Generator
from .__main__ import main

__all__ = ['GaugeRnR',
           'Component',
           'Result',
           'Distribution',
           'Settings',
           'Generator',
           'main', ]
