#!/usr/bin/env python3
import math

from . import QtObject
from ..core.signal import Signal


binding = """
    Binding { 
        target: // <id>.Layout; 
        property: "minimumWidth"; value: // <id>.layoutMinimumWidth 
    }
    Binding { 
        target: // <id>.Layout; 
        property: "maximumWidth"; value: // <id>.layoutMaximumWidth 
    }
    Binding { 
        target: // <id>.Layout; 
        property: "minimumHeight"; value: // <id>.layoutMinimumHeight
    }
    Binding { 
        target: // <id>.Layout; 
        property: "maximumHeight"; value: // <id>.layoutMaximumHeight 
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

        self.__height = None
        self.__min_height = None
        self.__max_height = None

        if self._base != 'Frame':
            self._QtObject__set_property(
                'property real layoutMinimumWidth', '0')
            self._QtObject__set_property(
                'property real layoutMaximumWidth', '-1')

            self._QtObject__set_property(
                'property real layoutMinimumHeight', '0')
            self._QtObject__set_property(
                'property real layoutMaximumHeight', '-1')

            self.qml = self.qml.replace('    // +', binding)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self._QtObject__name!r})'

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def height(self) -> tuple:
        """..."""
        return self.__height, self.__min_height, self.__max_height

    @height.setter
    def height(self, height: int | tuple) -> None:
        if not height:
            return
        
        height_ = None
        min_height = None
        max_height = None
        
        if isinstance(height, int): height = (height,)
        len_height = len(height)

        if len_height == 1:
            height_ = height[0]
        elif len_height == 2:
            height_, min_height = height
        else:
            height_, min_height, max_height = height[:3]

        if min_height is not None:
            if max_height and min_height > max_height: min_height = max_height
            if height_ and min_height > height_: min_height = height_
            self.__min_height = min_height

        elif self.__min_height is not None:
            if max_height and self.__min_height > max_height:
                self.__min_height = max_height
            if height_ and self.__min_height > height_:
                self.__min_height = height_
        
        if self._base == 'Frame':
            if height_ is not None:
                self._QtObject__set_property('height', height_)
            if min_height is not None:
                self._QtObject__set_property('minimumHeight', min_height)
            if max_height is not None:
                self._QtObject__set_property('maximumHeight', max_height)
            return

        if max_height is not None:
            self.__max_height = max_height

        if height_ is not None:
            self.__height = height_
            max_height = height_

        if not self._QtObject__obj:
            if min_height is not None:
                self._QtObject__set_property(
                    'property real layoutMinimumHeight', min_height)
            if max_height is not None:
                self._QtObject__set_property(
                    'property real layoutMaximumHeight', max_height)
        else:
            if min_height is not None:
                self._QtObject__set_property('layoutMinimumHeight', min_height)
            if max_height is not None:
                self._QtObject__set_property('layoutMaximumHeight', max_height)

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

        if self._base == 'Frame':
            if width_ is not None:
                self._QtObject__set_property('width', width_)
            if min_width is not None:
                self._QtObject__set_property('minimumWidth', min_width)
            if max_width is not None:
                self._QtObject__set_property('maximumWidth', max_width)
            return

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
