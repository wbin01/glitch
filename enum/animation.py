#!/usr/bin/env python3
from enum import Enum

from PySide6 import QtCore


class Animation(Enum):
    """Align enumeration."""
    FROM_LEFT = 'FROM_LEFT'
    FROM_RIGHT = 'FROM_RIGHT'
    FROM_TOP = 'FROM_TOP'
    FROM_BOTTOM = 'FROM_BOTTOM'
    CENTER = 'CENTER'
    CENTER_FROM_TOP = 'CENTER_FROM_TOP'
    CENTER_FROM_RIGHT = 'CENTER_FROM_RIGHT'
    CENTER_FROM_BOTTOM = 'CENTER_FROM_BOTTOM'
    CENTER_FROM_LEFT = 'CENTER_FROM_LEFT'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'
