#!/usr/bin/env python3
from PySide6 import QtGui
from __feature__ import snake_case


class Cursor(object):
    """Mouse cursor position."""
    def __init__(self) -> None:
        """Class constructor."""
        self.__cursor = QtGui.QCursor()
        self.__position = self.__cursor.pos()

    def position(self) -> tuple:
        """Tuple with mouse cursor position."""
        return self.__cursor.pos().x(), self.__cursor.pos().y()

    def x(self) -> int:
        """X mouse cursor position."""
        return self.__cursor.pos().x()

    def y(self) -> int:
        """Y mouse cursor position."""
        return self.__cursor.pos().y()

    def __str__(self):
        return f'<Cursor: {id(self)}>'
