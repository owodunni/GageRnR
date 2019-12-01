#!/usr/bin/env python3
import sys
import os
print(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GaugeRnR import GaugeRnR, Component, Result