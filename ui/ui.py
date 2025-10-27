#!/usr/bin/env python3
from . import QtObject
from ..core.signal import Signal


class UI(QtObject):
    """..."""
    def __init__(self, name: str = 'Item', *args, **kwargs) -> None:
        QtObject.__init__(self, name=name, *args, **kwargs)
        self.__base = 'UI'
        
        self.qml = self.qml + '  // Close ' + name
        self.__frame_signal = Signal()
        self.__frame = None

    @property
    def _frame(self):
        """..."""
        return self.__frame

    @property
    def _frame_signal(self) -> Signal:
        """..."""
        return self.__frame_signal

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self._QtObject__name!r})'

    def __str__(self) -> str:
        return self.__class__.__name__
