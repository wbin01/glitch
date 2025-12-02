#!/usr/bin/env python3
import math

from PySide6.QtQml import QQmlComponent, QQmlEngine, QQmlContext
from PySide6.QtCore import QUrl

from . import QtObject
from ..core.signal import Signal


binding_width = """
    Binding { 
        target: <id>.Layout; 
        property: "minimumWidth"; value: <id>.layoutMinimumWidth 
    }
    Binding { 
        target: <id>.Layout; 
        property: "maximumWidth"; value: <id>.layoutMaximumWidth 
    }
    // +
"""

binding_height = """
    Binding { 
        target: <id>.Layout; 
        property: "minimumHeight"; value: <id>.layoutMinimumHeight
    }
    Binding { 
        target: <id>.Layout; 
        property: "maximumHeight"; value: <id>.layoutMaximumHeight 
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

        # Signals
        self.__active_signal = Signal()
        self.__app_signal = Signal()
        self.__enabled_signal = Signal()
        self.__parent_signal = Signal()
        self.__visible_signal = Signal()
        
        # Properties
        self._QtObject__qml = self._QtObject__qml + '  // Close ' + name
        self.__app = None
        self.__parent = None

        self.__width = None
        self.__min_width = None
        self.__max_width = None

        self.__height = None
        self.__min_height = None
        self.__max_height = None

        # Flags
        self.__width_has_set = False
        self.__height_has_set = False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self._QtObject__name!r})'

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def enabled(self) -> bool:
        """..."""
        value = self._QtObject__property('enabled')
        if value is None:
            return True
        return value

    @enabled.setter
    def enabled(self, value: str) -> None:
        self._QtObject__set_property('enabled', value)
    
    @property
    def height(self) -> tuple:
        """..."""
        return self.__get_height()

    @height.setter
    def height(self, height: int | tuple) -> None:
        self.__set_height(height)

    @property
    def visible(self) -> bool:
        """..."""
        return self.__get_visible()

    @visible.setter
    def visible(self, value: str) -> None:
        self.__set_visible(value)

    @property
    def width(self) -> tuple:
        """..."""
        return self.__get_width()

    @width.setter
    def width(self, width: int | tuple) -> None:
        self.__set_width(width)

    @property
    def _active_signal(self) -> Signal:
        """..."""
        return self.__active_signal

    @property
    def _app_signal(self) -> Signal:
        """..."""
        return self.__app_signal

    @property
    def _enabled_signal(self) -> Signal:
        """..."""
        return self.__enabled_signal

    @property
    def _visible_signal(self) -> Signal:
        """..."""
        return self.__visible_signal

    @property
    def _app(self):
        """..."""
        return self.__app

    @property
    def _parent(self):
        """..."""
        return self.__parent

    @property
    def _base(self):
        """..."""
        return self.__base

    def __binding_obj(self, item, layout_prop, value, wh_type) -> bool:
        if not self.__width_has_set or not self.__height_has_set:
            engine = QQmlEngine.contextForObject(item).engine()
            qml_code = f"""
                import QtQuick
                import QtQuick.Layouts

                Binding {{
                    target: layoutTarget.Layout
                    property: "{layout_prop}"
                    value: bindingValue
                }}
            """

            component = QQmlComponent(engine)
            component.setData(qml_code.encode("utf-8"), QUrl())

            context = QQmlContext(engine.rootContext())
            context.setContextProperty('layoutTarget', item)
            context.setContextProperty('bindingValue', value)

            binding = component.create(context)
            binding.setParent(item)

            if wh_type == 'Width': self.__width_has_set = True
            if wh_type == 'Height': self.__height_has_set = True
            return True
        return False

    def __size(
            self, wh: int | tuple, wh_type: str,
            property_: int, property_min: int, property_max: int) -> tuple:
        if not wh: return property_, property_min, property_max

        # Values
        wh_, min_wh, max_wh = None, None, None
        if isinstance(wh, int): wh = (wh,)

        len_wh = len(wh)
        if len_wh == 1:
            wh_ = wh[0]
        elif len_wh == 2:
            wh_, min_wh = wh
        else:
            wh_, min_wh, max_wh = wh[:3]

        # Calibrate (When min is >)
        if min_wh is not None:
            if max_wh and min_wh > max_wh: min_wh = max_wh
            if wh_ and min_wh > wh_: min_wh = wh_
            property_min = min_wh

        elif property_min is not None:
            if max_wh and property_min > max_wh: property_min = max_wh
            if wh_ and property_min > wh_: property_min = wh_
        
        # Set for Frames
        if self._base == 'Frame':
            if wh_ is not None:
                self._QtObject__set_property(wh_type.lower(), wh_)
            if min_wh is not None:
                self._QtObject__set_property('minimum' + wh_type, min_wh)
            if max_wh is not None:
                self._QtObject__set_property('maximum' + wh_type, max_wh)
            return property_, property_min, property_max

        # Calibrate for Layouts and Views (ignore width: layouts use maximun)
        if max_wh is not None: property_max = max_wh
        if wh_ is not None: property_, max_wh = wh_, wh_
        
        # Set for Layouts and Views
        if not self._QtObject__obj:
            if min_wh is not None:
                self._QtObject__set_property(
                    'property real layoutMinimum' + wh_type, min_wh)
            if max_wh is not None:
                self._QtObject__set_property(
                    'property real layoutMaximum' + wh_type, max_wh)
            
            if min_wh or max_wh:
                if wh_type == 'Height' and not self.__height_has_set:
                    self._QtObject__qml = self._QtObject__qml.replace(
                    '// +', binding_height)
                    self.__height_has_set = True
                elif wh_type == 'Width' and not self.__width_has_set:
                    self._QtObject__qml = self._QtObject__qml.replace(
                        '// +', binding_width)
                    self.__width_has_set = True
        else:
            if min_wh is not None:
                if not self.__binding_obj(self._QtObject__obj,
                        'minimum' + wh_type, min_wh, wh_type):
                    self._QtObject__set_property(
                        'layoutMinimum' + wh_type, min_wh)
            if max_wh is not None:
                if not self.__binding_obj(self._QtObject__obj,
                        'maximum' + wh_type, max_wh, wh_type):
                    self._QtObject__set_property(
                        'layoutMaximum' + wh_type, max_wh)

        return property_, property_min, property_max

    def __get_visible(self) -> bool:
        """..."""
        value = self._QtObject__property('visible')
        if value is None:
            return True
        return value

    def __set_visible(self, value: str) -> None:
        self._QtObject__set_property('visible', value)

    def __get_width(self) -> tuple:
        """..."""
        width = self._QtObject__property('width')
        self.__width = int(width) if width else 0
        if self.__min_width: self.__min_width = int(self.__min_width)
        if self.__max_width: self.__max_width = int(self.__max_width)
        return self.__width, self.__min_width, self.__max_width

    def __set_width(self, width: int | tuple) -> None:
        self.__width, self.__min_width, self.__max_width = self.__size(
            width, 'Width', self.__width, self.__min_width, self.__max_width)

    def __get_height(self) -> tuple:
        """..."""
        height = self._QtObject__property('height')
        self.__height = int(height) if height else 0
        if self.__min_height: self.__min_height = int(self.__min_height)
        if self.__max_height: self.__max_height = int(self.__max_height)
        return self.__height, self.__min_height, self.__max_height

    def __set_height(self, height: int | tuple) -> None:
        self.__height, self.__min_height, self.__max_height = self.__size(
            height,'Height',self.__height, self.__min_height,self.__max_height)
