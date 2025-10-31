#!/usr/bin/env python3
from enum import Enum


class FrameShape(Enum):
    """Frame state enumeration."""
    # HIDDEN = 0 
    # AUTO = 1 
    FRAME = 2
    MAX = 4
    MIN = 3
    FULL = 5

    def __repr__(self) -> str:
        return self.__class__.__name__
