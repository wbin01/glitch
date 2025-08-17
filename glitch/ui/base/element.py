#!/usr/bin/env python3
import logging

from .mixin import MarginsMixin
from .ui import UI
from ...core.signal import Signal
from ...enum import Size


class Element(MarginsMixin, UI):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.size_signal = Signal()

        self.__fill_height = False
        self.__fill_width = True
        self.__height = 30
        self.__width = 100
        self.__size = self.__width, self.__height
        self.__margins = 0, 0, 0, 0

        self.class_id('Element')

    @property
    def size(self) -> tuple:
        """Frame width and height.

        Tuple like (100, 30).

        It is not mandatory to pass all the values, the last value will be 
        used to fill in the missing ones:

        `size = 100` is equivalent to `margins = 100, 100`

        Use `Size.AUTO` enum (or `None`) for a value to be automatic.
        `Size.AUTO` indicates that the value is the same as before. Example:

            # Change only the height
            `size = Size.AUTO, 50

            # Change only the width
            `size = 100, Size.AUTO

        Use `Size.FILL` to completely fill the space. Example:

            # Horizontal fill
            `size = Size.FILL, 30

            # Vertical fill
            `size = 100, Size.FILL
        """
        return self.__size

    @size.setter
    def size(self, size: str | tuple) -> None:
        if isinstance(size, str):
            size = int(size) if size.isdigit() else size.split(',')

        if isinstance(size, int):
            width, height = size, size
        elif len(size) == 1:
            width, height = size[0], size[0]
        elif len(size) >= 2:
            width, height = size[:2]

        width = Size.AUTO if width is None else width
        height = Size.AUTO if height is None else height

        enum_w = width if isinstance(width, Size) else False
        enum_h = height if isinstance(height, Size) else False
        width = self.__size[0] if not isinstance(width, int) else width
        height = self.__size[1] if not isinstance(height, int) else height

        if self._obj:
            self.__set_obj_size(enum_w, 'width', width)
            self.__set_obj_size(enum_h, 'height', height)
        else:
            self.__set_qml_size(enum_w, 'width', width)
            self.__set_qml_size(enum_h, 'height', height)

        self.__width = width
        self.__height = height
        self.__size = width, height
        self.size_signal.emit()

    def __set_obj_size(
            self, enum: Size, width_height: 'width', value: int) -> None:
        fill = 'fillWidth' if width_height == 'width' else 'fillHeight'
        if enum:
            if enum == Size.FILL:
                self._obj.setProperty(fill, True)

            elif not self._obj.property(fill):
                self._obj.setProperty(width_height, value)
        else:
            self._obj.setProperty(fill, False)
            self._obj.setProperty(width_height, value)

    def __set_qml_size(
            self, enum: Size, width_height: 'width', value: int) -> None:
        fill = 'fillWidth' if width_height == 'width' else 'fillHeight'
        old_value = self.__width if width_height == 'width' else self.__height

        if enum:
            if enum == Size.FILL:
                self._qml = self._qml.replace(f'{fill}: false',f'{fill}: true')

            elif f'property bool {fill}: false' in self._qml:
                self._qml = self._qml.replace(
                    f'{width_height}: {old_value}', f'{width_height}: {value}')
        else:
            self._qml = self._qml.replace(
                f'{fill}: true', f'{fill}: false').replace(
                    f'{width_height}: {old_value}', f'{width_height}: {value}')

    def __str__(self) -> str:
        return "<class 'Element'>"
