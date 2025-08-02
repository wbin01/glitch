#!/usr/bin/env python3
from enum import Enum


class FrameState(Enum):
    """Frame state enumeration."""
    # HIDDEN = 0 
    # AUTO = 1 
    FRAME = 2
    MAXIMIZED = 4
    MINIMIZED = 3
    FULL_SCREEN = 5

    def __str__(self) -> str:
        return "<class 'FrameState'>"
