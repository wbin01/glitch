#!/usr/bin/env python3
from enum import Enum

from PySide6 import QtCore


class FrameControl(Enum):
    """Frame action enumeration."""
    CLOSE = 'CLOSE'
    MAX = 'MAX'
    MIN = 'MIN'
    FULL = 'FULL'
    
    def __str__(self) -> str:
        return "<class 'FrameAction'>"
