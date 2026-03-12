#!/usr/bin/env python3
"""Graphical interface launcher for Plakoto game."""

import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from plakoto.interfaces.graphical_interface import GraphicalInterface


def main():
    gui = GraphicalInterface()
    gui.run()


if __name__ == "__main__":
    main()
