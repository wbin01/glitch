#!/usr/bin/env python3
from enum import Enum

from PySide6 import QtCore


class Align(Enum):
    """Align enumeration."""
    BASE_LINE = QtCore.Qt.AlignBaseline
    BOTTOM = QtCore.Qt.AlignBottom
    BOTTOM_LEFT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft
    BOTTOM_RIGHT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
    CENTER = QtCore.Qt.AlignCenter
    H_CENTER = QtCore.Qt.AlignHCenter
    JUSTIFY = QtCore.Qt.AlignJustify
    LEFT = QtCore.Qt.AlignLeft
    RIGHT = QtCore.Qt.AlignRight
    TOP = QtCore.Qt.AlignTop
    TOP_LEFT = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
    TOP_RIGHT = QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
    V_CENTER = QtCore.Qt.AlignVCenter
    
    def __str__(self):
        return f'<Align: {id(self)}>'
