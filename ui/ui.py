#!/usr/bin/env python3
from . import QtObject
from ..core.signal import Signal


class UI(QtObject):
    """..."""
    def __init__(self, name: str = 'Item', *args, **kwargs) -> None:
        QtObject.__init__(self, name=name, *args, **kwargs)
        self._base = 'UI'
        
        self.qml = self.qml + '  // Close ' + name
        self.__app_signal = Signal()
        self.__app = None

    @property
    def _app(self):
        """..."""
        return self.__app

    @property
    def _app_signal(self) -> Signal:
        """..."""
        return self.__app_signal

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self._QtObject__name!r})'

    def __str__(self) -> str:
        return self.__class__.__name__
