#/usr/bin/env python3
from PySide6 import QtQuick, QtCore  # QtGui, QtQml 

from .element import Element


class Button(Element):
    """..."""
    def __init__(
            self, qt_quick_item: QtQuick.QQuickItem, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__obj = qt_quick_item
        self.__text = self.__obj.property('text')
        self.__icon = self.__obj.findChild(QtCore.QObject, 'icon')
        # iconSource

    @property
    def text(self) -> str:
        return self.__obj.property('text')

    @text.setter
    def text(self, text: str) -> None:
        self.__obj.setProperty('text', text)

    def connect(self, func: callable) -> None:
        self.__obj.clicked.connect(func)
