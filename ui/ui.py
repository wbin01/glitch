#!/usr/bin/env python3
import math

from . import QtObject
from ..core.signal import Signal


class UI(QtObject):
    """..."""
    def __init__(self, name: str = 'Item', *args, **kwargs) -> None:
        super().__init__(name=name, *args, **kwargs)
        self.__base = 'UI'
        
        self.qml = self.qml + '  // Close ' + name
        self.__app_signal = Signal()
        self.__app = None
        
        self.__width = None
        self.__min_width = None
        self.__max_width = None

        self._QtObject__set_property(
            'property real minimumWidth', 'Layout.minimumWidth')
        self._QtObject__set_property(
            'property real maximumWidth', 'Layout.maximumWidth')
        self._QtObject__set_property(
            'property real minimumHeight', 'Layout.minimumHeight')
        self._QtObject__set_property(
            'property real maximumHeight', 'Layout.maximumHeight')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self._QtObject__name!r})'

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def height(self) -> tuple:
        """..."""
        pass

    @height.setter
    def height(self, height: int | tuple) -> None:
        pass

    @property
    def width(self) -> tuple:
        """..."""
        return self.__width, self.__min_width, self.__max_width

    @width.setter
    def width(self, width: int | tuple) -> None:
        if not width:
            return

        if isinstance(width, int):
            self._QtObject__set_property('width', width)
            if not self._QtObject__obj:
                self._QtObject__set_property('Layout.maximumWidth', width)
            else:
                self._QtObject__set_property('maximumWidth', width)
            self.__width = width
            return

        len_width = len(width)
        width_ = None
        min_width = None
        max_width = None

        if len_width == 1:
            width_ = width[0]
        elif len_width == 2:
            width_, min_width = width
        else:
            width_, min_width, max_width = width[:3]

        if width_ is not None:
            self._QtObject__set_property('width', width_)
            self.__width = width_
            max_width = width_

        if min_width is not None:
            if min_width is False: min_width = 0
            if not self._QtObject__obj:
                self._QtObject__set_property('Layout.minimumWidth', min_width)
            else:
                self._QtObject__set_property('minimumWidth', min_width)
            self.__min_width = min_width

        if max_width is not None:
            if max_width is False: max_width = 0
            if not self._QtObject__obj:
                self._QtObject__set_property('Layout.maximumWidth', max_width)
            else:
                self._QtObject__set_property('maximumWidth', max_width)
            self.__max_width = max_width

    @property
    def _app(self):
        """..."""
        return self.__app

    @property
    def _app_signal(self) -> Signal:
        """..."""
        return self.__app_signal

    @property
    def _base(self):
        """..."""
        return self.__base
