#!/usr/bin/env python3
import math

from . import QtObject
from ..core.signal import Signal


binding = """
    Binding { 
        target: // <id>.Layout; 
        property: "minimumWidth"; 
        value: // <id>.layoutMinimumWidth 
    }
    Binding { 
        target: // <id>.Layout; 
        property: "maximumWidth"; 
        value: // <id>.layoutMaximumWidth 
    }
    // +
"""


class UI(QtObject):
    """..."""
    def __init__(
            self, name: str = 'Item', base: str = 'UI',
            *args, **kwargs) -> None:
        super().__init__(name=name, base=base, *args, **kwargs)
        self.__base = base
        
        self.qml = self.qml + '  // Close ' + name
        self.__app_signal = Signal()
        self.__app = None
        
        self.__width = None
        self.__min_width = None
        self.__max_width = None

        self.__set_min_width = False
        self.__set_max_width = False

        if self._base == 'View':
            self._QtObject__set_property(
                'property real layoutMinimumWidth', '0')
            self._QtObject__set_property(
                'property real layoutMaximumWidth', '-1')

            self.qml = self.qml.replace('    // +', binding)

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
        
        width_ = None
        min_width = None
        max_width = None
        
        if isinstance(width, int): width = (width,)
        len_width = len(width)

        if len_width == 1:
            width_ = width[0]
        elif len_width == 2:
            width_, min_width = width
        else:
            width_, min_width, max_width = width[:3]

        if min_width is not None:
            if max_width and min_width > max_width: min_width = max_width
            if width_ and min_width > width_: min_width = width_
            self.__min_width = min_width

        elif self.__min_width is not None:
            if max_width and self.__min_width > max_width:
                self.__min_width = max_width
            if width_ and self.__min_width > width_: self.__min_width = width_
    

        if max_width is not None:
            self.__max_width = max_width

        if width_ is not None:
            self.__width = width_
            max_width = width_

        if not self._QtObject__obj:
            if min_width is not None:
                self._QtObject__set_property(
                    'property real layoutMinimumWidth', min_width)
            if max_width is not None:
                self._QtObject__set_property(
                    'property real layoutMaximumWidth', max_width)
        else:
            if min_width is not None:
                self._QtObject__set_property('layoutMinimumWidth', min_width)
            if max_width is not None:
                self._QtObject__set_property('layoutMaximumWidth', max_width)

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
