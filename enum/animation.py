#!/usr/bin/env python3
from enum import Enum

from PySide6 import QtCore


class Animation(Enum):
    """Align enumeration."""
    FROM_LEFT = 'FROM_LEFT'
    FROM_RIGHT = 'FROM_RIGHT'
    FROM_TOP = 'FROM_TOP'
    FROM_BOTTOM = 'FROM_BOTTOM'
    # FROM_CENTER = 'FROM_CENTER'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'
