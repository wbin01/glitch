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
        self.__height, self.__min_height, self.__max_height = self.__w_or_h(
            height, 'Height',
            self.__height, self.__min_height, self.__max_height)

    @property
    def width(self) -> tuple:
        """..."""
        return self.__width, self.__min_width, self.__max_width

    @width.setter
    def width(self, width: int | tuple) -> None:
        self.__width, self.__min_width, self.__max_width = self.__w_or_h(
            width, 'Width', self.__width, self.__min_width, self.__max_width)

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

    def __w_or_h(
            self, wh: int | tuple, wh_type: str,
            property_: int, property_min: int, property_max: int) -> tuple:
        if not wh: return

        # Values
        wh_ = None
        min_wh = None
        max_wh = None
        
        if isinstance(wh, int): wh = (wh,)
        len_wh = len(wh)

        if len_wh == 1:
            wh_ = wh[0]
        elif len_wh == 2:
            wh_, min_wh = wh
        else:
            wh_, min_wh, max_wh = wh[:3]

        # Calibrate values
        if min_wh is not None:
            if max_wh and min_wh > max_wh: min_wh = max_wh
            if wh_ and min_wh > wh_: min_wh = wh_
            property_min = min_wh

        elif property_min is not None:
            if max_wh and property_min > max_wh:
                property_min = max_wh
            if wh_ and property_min > wh_:
                property_min = wh_
        
        # Set for Frames
        if self._base == 'Frame':
            if wh_ is not None:
                self._QtObject__set_property(wh_type.lower(), wh_)
            if min_wh is not None:
                self._QtObject__set_property('minimum' + wh_type, min_wh)
            if max_wh is not None:
                self._QtObject__set_property('maximum' + wh_type, max_wh)
            return property_, property_min, property_max

        # Set for Layouts and Views (ignore width and use maximun on layouts)
        if max_wh is not None:
            property_max = max_wh

        if wh_ is not None:
            property_ = wh_
            max_wh = wh_

        if not self._QtObject__obj:
            if min_wh is not None:
                self._QtObject__set_property(
                    'property real layoutMinimum' + wh_type, min_wh)
            if max_wh is not None:
                self._QtObject__set_property(
                    'property real layoutMaximum' + wh_type, max_wh)
        else:
            if min_wh is not None:
                self._QtObject__set_property('layoutMinimum' + wh_type, min_wh)
            if max_wh is not None:
                self._QtObject__set_property('layoutMaximum' + wh_type, max_wh)

        return property_, property_min, property_max
