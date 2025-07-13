#/usr/bin/env python3
from PySide6 import QtCore

from .element import Element
from ..enum.event import Event


class Button(Element):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = self._obj.property('text')
        self.__icon = self._obj.findChild(QtCore.QObject, 'icon')
        # iconSource

    @property
    def text(self) -> str:
        """..."""
        return self._obj.property('text')

    @text.setter
    def text(self, text: str) -> None:
        self._obj.setProperty('text', text)

    @property
    def icon(self) -> str:
        """..."""
        return self.__icon

    @icon.setter
    def icon(self, name: str) -> None:
        self._obj.setProperty('icon', name)

    def connect(
            self, method: callable, event: Event = Event.MOUSE_PRESS) -> None:
        """..."""
        if event == Event.MOUSE_PRESS:
            self._obj.clicked.connect(method)
