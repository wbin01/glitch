#!/usr/bin/env python3
from enum import Enum


class Shape(Enum):
    """Frame shape enumeration."""
    # 0: Window.Hidden
    # 1: Window.AutomaticVisibility (default - normally Windowed)
    # 2: Window.Windowed
    # 3: Window.Minimized
    # 4: Window.Maximized
    # 5: Window.FullScreen
    HIDDEN = 0
    AUTO = 1
    FRAME = 2
    MAX = 4
    MIN = 3
    FULL = 5

    def __repr__(self) -> str:
        return self.__class__.__name__
